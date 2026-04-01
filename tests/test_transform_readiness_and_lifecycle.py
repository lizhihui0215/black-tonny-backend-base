import json
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import CaptureBase
from src.app.crud.crud_capture_batches import crud_capture_batches
from src.app.crud.crud_capture_endpoint_payloads import crud_capture_endpoint_payloads
from src.app.schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
)
from src.app.schemas.transform import AdmittedTransformInputSnapshot, TransformReadinessDecision
from src.app.services.admitted_transform_selector import select_admitted_transform_input
from src.app.services.capture_batch_lifecycle import (
    mark_capture_batch_failed,
    mark_capture_batch_transformed,
)
from src.app.services.transform_readiness_evaluator import evaluate_sales_orders_transform_readiness


def dump_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def as_naive_utc(value: datetime) -> datetime:
    return value.astimezone(UTC).replace(tzinfo=None) if value.tzinfo is not None else value


@pytest_asyncio.fixture
async def capture_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "transform_readiness_and_lifecycle.sqlite3"
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


async def create_batch(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    batch_status: str = "queued",
    transformed_at: datetime | None = None,
    error_message: str | None = None,
) -> None:
    await crud_capture_batches.create(
        db=db,
        object=CaptureBatchCreate(
            capture_batch_id=capture_batch_id,
            batch_status=batch_status,
            source_name="yeusoft.capture",
            transformed_at=transformed_at,
            error_message=error_message,
        ),
        schema_to_select=CaptureBatchRead,
    )


async def append_payload(
    db: AsyncSession,
    *,
    capture_batch_id: str,
    source_endpoint: str,
    payload: object,
    pulled_at: datetime,
) -> None:
    payload_json = dump_json(payload)

    await crud_capture_endpoint_payloads.create(
        db=db,
        object=CaptureEndpointPayloadCreate(
            capture_batch_id=capture_batch_id,
            source_endpoint=source_endpoint,
            payload_json=payload_json,
            checksum=f"checksum-{source_endpoint}",
            pulled_at=pulled_at,
        ),
        schema_to_select=CaptureEndpointPayloadRead,
    )


async def build_admitted_input(
    db: AsyncSession,
    *,
    capture_batch_id: str,
) -> AdmittedTransformInputSnapshot:
    selected = await select_admitted_transform_input(
        db=db,
        capture_batch_id=capture_batch_id,
    )

    assert isinstance(selected, AdmittedTransformInputSnapshot)
    return selected


@pytest.mark.asyncio
async def test_sales_orders_transform_readiness_returns_ready_for_first_slice_bundle(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-ready",
        batch_status="captured",
        error_message="kept as persisted context",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-ready",
        source_endpoint="/erp/orders",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 6, tzinfo=UTC),
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-ready",
        source_endpoint="/erp/inventory",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 7, tzinfo=UTC),
    )

    admitted_input = await build_admitted_input(
        capture_db_session,
        capture_batch_id="capture-ready",
    )
    decision = evaluate_sales_orders_transform_readiness(admitted_input)

    assert isinstance(decision, TransformReadinessDecision)
    assert decision.capture_batch_id == "capture-ready"
    assert decision.slice_name == "sales_orders"
    assert decision.is_ready is True
    assert decision.reason == "ready"
    assert decision.matched_payload_count == 1


@pytest.mark.asyncio
async def test_sales_orders_transform_readiness_requires_matching_sales_payloads(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-no-sales",
        batch_status="captured",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-no-sales",
        source_endpoint="/erp/inventory",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 8, tzinfo=UTC),
    )

    admitted_input = await build_admitted_input(
        capture_db_session,
        capture_batch_id="capture-no-sales",
    )
    decision = evaluate_sales_orders_transform_readiness(admitted_input)

    assert decision.is_ready is False
    assert decision.reason == "missing_sales_orders_payloads"
    assert decision.matched_payload_count == 0


@pytest.mark.asyncio
async def test_sales_orders_transform_readiness_requires_captured_batch_status(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-queued",
        batch_status="queued",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-queued",
        source_endpoint="/erp/orders",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 9, tzinfo=UTC),
    )

    admitted_input = await build_admitted_input(
        capture_db_session,
        capture_batch_id="capture-queued",
    )
    decision = evaluate_sales_orders_transform_readiness(admitted_input)

    assert decision.is_ready is False
    assert decision.reason == "batch_status_not_captured"
    assert decision.matched_payload_count == 1


@pytest.mark.asyncio
async def test_sales_orders_transform_readiness_rejects_already_transformed_batches(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-transformed",
        batch_status="captured",
        transformed_at=datetime(2026, 4, 10, tzinfo=UTC),
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-transformed",
        source_endpoint="/erp/orders",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 11, tzinfo=UTC),
    )

    admitted_input = await build_admitted_input(
        capture_db_session,
        capture_batch_id="capture-transformed",
    )
    decision = evaluate_sales_orders_transform_readiness(admitted_input)

    assert decision.is_ready is False
    assert decision.reason == "already_transformed"
    assert decision.matched_payload_count == 1


@pytest.mark.asyncio
async def test_mark_capture_batch_transformed_preserves_error_message_and_sets_timestamp(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-mark-transformed",
        batch_status="captured",
        error_message="kept for traceability",
    )

    before_mark = datetime.now(UTC)
    updated_batch = await mark_capture_batch_transformed(
        capture_db_session,
        capture_batch_id="capture-mark-transformed",
    )
    after_mark = datetime.now(UTC)

    assert updated_batch is not None
    assert updated_batch.batch_status == "transformed"
    assert updated_batch.transformed_at is not None
    assert as_naive_utc(before_mark) <= updated_batch.transformed_at <= as_naive_utc(after_mark)
    assert updated_batch.error_message == "kept for traceability"


@pytest.mark.asyncio
async def test_mark_capture_batch_failed_overwrites_error_message_without_setting_transformed_at(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-mark-failed",
        batch_status="captured",
        error_message="older error",
    )

    updated_batch = await mark_capture_batch_failed(
        capture_db_session,
        capture_batch_id="capture-mark-failed",
        error_message="latest transform failure",
    )

    assert updated_batch is not None
    assert updated_batch.batch_status == "failed"
    assert updated_batch.transformed_at is None
    assert updated_batch.error_message == "latest transform failure"


@pytest.mark.asyncio
async def test_capture_batch_lifecycle_helper_rejects_non_captured_source_state(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-invalid-transition",
        batch_status="queued",
    )

    with pytest.raises(ValueError, match="captured state"):
        await mark_capture_batch_transformed(
            capture_db_session,
            capture_batch_id="capture-invalid-transition",
        )

    with pytest.raises(ValueError, match="captured state"):
        await mark_capture_batch_failed(
            capture_db_session,
            capture_batch_id="capture-invalid-transition",
            error_message="latest transform failure",
        )


@pytest.mark.asyncio
async def test_capture_batch_lifecycle_helper_returns_none_for_missing_batch(
    capture_db_session: AsyncSession,
) -> None:
    assert (
        await mark_capture_batch_transformed(
            capture_db_session,
            capture_batch_id="missing-batch",
        )
        is None
    )
    assert (
        await mark_capture_batch_failed(
            capture_db_session,
            capture_batch_id="missing-batch",
            error_message="latest transform failure",
        )
        is None
    )
