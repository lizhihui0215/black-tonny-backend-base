import json
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import CaptureBase, ServingBase
from src.app.crud.crud_analysis_batches import crud_analysis_batches
from src.app.crud.crud_capture_batches import crud_capture_batches, get_capture_batch_read
from src.app.crud.crud_capture_endpoint_payloads import crud_capture_endpoint_payloads
from src.app.crud.crud_sales_orders import get_sales_order_read_by_projection_key, list_sales_order_reads
from src.app.schemas.analysis import AnalysisBatchCreate, AnalysisBatchRead
from src.app.schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
)
from src.app.schemas.transform import CaptureToSalesOrdersPathResult
from src.app.services.capture_to_sales_orders_path import run_capture_to_sales_orders_path


def dump_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


@pytest_asyncio.fixture
async def capture_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "capture_to_sales_orders_path_capture.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection: object, _connection_record: object) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as connection:
        await connection.run_sync(CaptureBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def serving_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "capture_to_sales_orders_path_serving.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    async with engine.begin() as connection:
        await connection.run_sync(ServingBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


async def create_capture_batch(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    batch_status: str = "captured",
    error_message: str | None = None,
) -> None:
    await crud_capture_batches.create(
        db=db,
        object=CaptureBatchCreate(
            capture_batch_id=capture_batch_id,
            batch_status=batch_status,
            source_name="yeusoft.capture",
            error_message=error_message,
        ),
        schema_to_select=CaptureBatchRead,
    )


async def create_analysis_batch(
    db: AsyncSession,
    *,
    analysis_batch_id: str,
    capture_batch_id: str,
) -> None:
    await crud_analysis_batches.create(
        db=db,
        object=AnalysisBatchCreate(
            analysis_batch_id=analysis_batch_id,
            capture_batch_id=capture_batch_id,
            batch_status="queued",
            source_endpoint="/erp/orders",
        ),
        schema_to_select=AnalysisBatchRead,
    )


async def append_payload(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    source_endpoint: str,
    payload: object,
    pulled_at: datetime,
) -> None:
    await crud_capture_endpoint_payloads.create(
        db=db,
        object=CaptureEndpointPayloadCreate(
            capture_batch_id=capture_batch_id,
            source_endpoint=source_endpoint,
            payload_json=dump_json(payload),
            checksum=f"checksum-{capture_batch_id}-{source_endpoint}-{pulled_at.isoformat()}",
            pulled_at=pulled_at,
        ),
        schema_to_select=CaptureEndpointPayloadRead,
    )


@pytest.mark.asyncio
async def test_capture_to_sales_orders_path_applies_contract_and_marks_batch_transformed(
    capture_db_session: AsyncSession,
    serving_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        capture_db_session,
        capture_batch_id="capture-success",
        batch_status="captured",
        error_message="keep for diagnostics",
    )
    await create_analysis_batch(
        capture_db_session,
        analysis_batch_id="analysis-001",
        capture_batch_id="capture-success",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-success",
        source_endpoint="/erp/orders",
        payload={
            "rows": [
                {
                    "order_id": "order-001",
                    "store_id": "store-001",
                    "paid_at": "2026-04-17T00:00:00+00:00",
                    "paid_amount": "100.50",
                    "payment_status": "paid",
                }
            ]
        },
        pulled_at=datetime(2026, 4, 17, tzinfo=UTC),
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-success",
        source_endpoint="/erp/orders",
        payload={
            "rows": [
                {
                    "order_id": "order-001",
                    "store_id": "store-002",
                    "paid_at": "2026-04-18T00:00:00+00:00",
                    "paid_amount": "120.00",
                    "payment_status": "refunded",
                },
                {
                    "order_id": "order-002",
                    "paid_at": "2026-04-18T08:00:00+00:00",
                    "paid_amount": "60.00",
                    "payment_status": "paid",
                },
            ]
        },
        pulled_at=datetime(2026, 4, 18, tzinfo=UTC),
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-success",
        source_endpoint="/erp/inventory",
        payload={"rows": [{"sku_id": "sku-001"}]},
        pulled_at=datetime(2026, 4, 18, tzinfo=UTC),
    )

    result = await run_capture_to_sales_orders_path(
        capture_db_session,
        serving_db_session,
        capture_batch_id="capture-success",
    )
    transformed_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="capture-success",
    )
    order_001 = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )
    order_002 = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-002",
    )

    assert isinstance(result, CaptureToSalesOrdersPathResult)
    assert result.status == "succeeded"
    assert result.reason == "applied"
    assert result.readiness_decision is not None
    assert result.readiness_decision.reason == "ready"
    assert result.analysis_batch_id == "analysis-001"
    assert result.projection_result is not None
    assert result.projection_result.applied_count == 2
    assert result.projection_result.inserted_count == 2
    assert result.projection_result.updated_count == 0
    assert result.lifecycle_batch is not None
    assert result.lifecycle_batch.batch_status == "transformed"
    assert result.lifecycle_batch.transformed_at is not None
    assert result.lifecycle_batch.error_message == "keep for diagnostics"

    assert transformed_batch is not None
    assert transformed_batch.batch_status == "transformed"
    assert transformed_batch.error_message == "keep for diagnostics"

    assert order_001 is not None
    assert order_001.capture_batch_id == "capture-success"
    assert order_001.store_id == "store-002"
    assert order_001.paid_amount == Decimal("120.00")
    assert order_001.payment_status == "refunded"

    assert order_002 is not None
    assert order_002.store_id is None
    assert order_002.paid_amount == Decimal("60.00")
    assert order_002.payment_status == "paid"


@pytest.mark.asyncio
async def test_capture_to_sales_orders_path_returns_noop_when_selector_returns_none(
    capture_db_session: AsyncSession,
    serving_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        capture_db_session,
        capture_batch_id="capture-noop",
        batch_status="captured",
    )
    await create_analysis_batch(
        capture_db_session,
        analysis_batch_id="analysis-001",
        capture_batch_id="capture-noop",
    )

    result = await run_capture_to_sales_orders_path(
        capture_db_session,
        serving_db_session,
        capture_batch_id="capture-noop",
    )
    persisted_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="capture-noop",
    )
    sales_rows = await list_sales_order_reads(serving_db_session, limit=None)

    assert result.status == "noop"
    assert result.reason == "missing_admitted_input"
    assert result.readiness_decision is None
    assert result.projection_result is None
    assert result.lifecycle_batch is None
    assert persisted_batch is not None
    assert persisted_batch.batch_status == "captured"
    assert persisted_batch.transformed_at is None
    assert sales_rows["data"] == []
    assert sales_rows["total_count"] == 0


@pytest.mark.asyncio
async def test_capture_to_sales_orders_path_returns_non_ready_without_writes(
    capture_db_session: AsyncSession,
    serving_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        capture_db_session,
        capture_batch_id="capture-non-ready",
        batch_status="captured",
    )
    await create_analysis_batch(
        capture_db_session,
        analysis_batch_id="analysis-001",
        capture_batch_id="capture-non-ready",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-non-ready",
        source_endpoint="/erp/inventory",
        payload={"rows": [{"sku_id": "sku-001"}]},
        pulled_at=datetime(2026, 4, 19, tzinfo=UTC),
    )

    result = await run_capture_to_sales_orders_path(
        capture_db_session,
        serving_db_session,
        capture_batch_id="capture-non-ready",
    )
    persisted_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="capture-non-ready",
    )
    sales_rows = await list_sales_order_reads(serving_db_session, limit=None)

    assert result.status == "non_ready"
    assert result.reason == "not_ready"
    assert result.readiness_decision is not None
    assert result.readiness_decision.reason == "missing_sales_orders_payloads"
    assert result.projection_result is None
    assert result.lifecycle_batch is None
    assert persisted_batch is not None
    assert persisted_batch.batch_status == "captured"
    assert sales_rows["data"] == []
    assert sales_rows["total_count"] == 0


@pytest.mark.asyncio
async def test_capture_to_sales_orders_path_marks_failed_when_analysis_context_is_missing(
    capture_db_session: AsyncSession,
    serving_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        capture_db_session,
        capture_batch_id="capture-missing-analysis",
        batch_status="captured",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-missing-analysis",
        source_endpoint="/erp/orders",
        payload={
            "rows": [
                {
                    "order_id": "order-001",
                    "paid_at": "2026-04-20T00:00:00+00:00",
                    "paid_amount": "90.00",
                    "payment_status": "paid",
                }
            ]
        },
        pulled_at=datetime(2026, 4, 20, tzinfo=UTC),
    )

    result = await run_capture_to_sales_orders_path(
        capture_db_session,
        serving_db_session,
        capture_batch_id="capture-missing-analysis",
    )
    failed_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="capture-missing-analysis",
    )
    sales_rows = await list_sales_order_reads(serving_db_session, limit=None)

    assert result.status == "failed"
    assert result.reason == "missing_analysis_batch"
    assert result.readiness_decision is not None
    assert result.readiness_decision.reason == "ready"
    assert result.lifecycle_batch is not None
    assert result.lifecycle_batch.batch_status == "failed"
    assert result.failure_message is not None
    assert "requires one linked `analysis_batches` row" in result.failure_message
    assert failed_batch is not None
    assert failed_batch.batch_status == "failed"
    assert failed_batch.transformed_at is None
    assert failed_batch.error_message == result.failure_message
    assert sales_rows["data"] == []
    assert sales_rows["total_count"] == 0


@pytest.mark.asyncio
async def test_capture_to_sales_orders_path_marks_failed_when_projection_contract_apply_raises(
    capture_db_session: AsyncSession,
    serving_db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await create_capture_batch(
        capture_db_session,
        capture_batch_id="capture-contract-failure",
        batch_status="captured",
    )
    await create_analysis_batch(
        capture_db_session,
        analysis_batch_id="analysis-001",
        capture_batch_id="capture-contract-failure",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-contract-failure",
        source_endpoint="/erp/orders",
        payload={
            "rows": [
                {
                    "order_id": "order-001",
                    "paid_at": "2026-04-21T00:00:00+00:00",
                    "paid_amount": "100.00",
                    "payment_status": "paid",
                }
            ]
        },
        pulled_at=datetime(2026, 4, 21, tzinfo=UTC),
    )

    async def _raise_contract_error(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("contract exploded")

    monkeypatch.setattr(
        "src.app.services.capture_to_sales_orders_path.apply_sales_orders_projection_contract",
        _raise_contract_error,
    )

    result = await run_capture_to_sales_orders_path(
        capture_db_session,
        serving_db_session,
        capture_batch_id="capture-contract-failure",
    )
    failed_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="capture-contract-failure",
    )
    sales_rows = await list_sales_order_reads(serving_db_session, limit=None)

    assert result.status == "failed"
    assert result.reason == "projection_contract_apply_failed"
    assert result.readiness_decision is not None
    assert result.readiness_decision.reason == "ready"
    assert result.analysis_batch_id == "analysis-001"
    assert result.projection_result is None
    assert result.lifecycle_batch is not None
    assert result.lifecycle_batch.batch_status == "failed"
    assert result.failure_message is not None
    assert "contract exploded" in result.failure_message
    assert failed_batch is not None
    assert failed_batch.batch_status == "failed"
    assert failed_batch.transformed_at is None
    assert failed_batch.error_message == result.failure_message
    assert sales_rows["data"] == []
    assert sales_rows["total_count"] == 0
