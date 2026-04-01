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
from src.app.schemas.transform import AdmittedTransformInputSnapshot
from src.app.services.admitted_transform_selector import select_admitted_transform_input


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
    db_path = tmp_path / "admitted_transform_selector.sqlite3"
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


@pytest.mark.asyncio
async def test_select_admitted_transform_input_returns_structural_bundle_without_analysis_dependency(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-001",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-001",
        source_endpoint="/erp/orders",
        payload={"page": 1},
        pulled_at=datetime(2026, 4, 2, tzinfo=UTC),
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-001",
        source_endpoint="/erp/orders",
        payload={"page": 2},
        pulled_at=datetime(2026, 4, 3, tzinfo=UTC),
    )

    selected = await select_admitted_transform_input(
        db=capture_db_session,
        capture_batch_id="capture-001",
    )

    assert isinstance(selected, AdmittedTransformInputSnapshot)
    assert selected.batch.capture_batch_id == "capture-001"
    assert selected.batch.batch_status == "queued"
    assert selected.batch.transformed_at is None
    assert selected.batch.error_message is None
    assert [payload.payload_json for payload in selected.payloads] == [
        '{"page":1}',
        '{"page":2}',
    ]


@pytest.mark.asyncio
async def test_select_admitted_transform_input_returns_none_when_batch_has_no_linked_payloads(
    capture_db_session: AsyncSession,
) -> None:
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-empty",
    )

    selected = await select_admitted_transform_input(
        db=capture_db_session,
        capture_batch_id="capture-empty",
    )

    assert selected is None


@pytest.mark.asyncio
async def test_select_admitted_transform_input_keeps_selection_structural_without_status_or_transition_gates(
    capture_db_session: AsyncSession,
) -> None:
    transformed_at = datetime(2026, 4, 4, tzinfo=UTC)
    await create_batch(
        capture_db_session,
        capture_batch_id="capture-structural",
        batch_status="failed",
        transformed_at=transformed_at,
        error_message="kept for diagnostics",
    )
    await append_payload(
        capture_db_session,
        capture_batch_id="capture-structural",
        source_endpoint="/erp/orders",
        payload={"items": [1, 2]},
        pulled_at=datetime(2026, 4, 5, tzinfo=UTC),
    )

    selected = await select_admitted_transform_input(
        db=capture_db_session,
        capture_batch_id="capture-structural",
    )

    assert isinstance(selected, AdmittedTransformInputSnapshot)
    assert selected.batch.batch_status == "failed"
    assert selected.batch.transformed_at is not None
    assert as_naive_utc(selected.batch.transformed_at) == as_naive_utc(transformed_at)
    assert selected.batch.error_message == "kept for diagnostics"
    assert [payload.source_endpoint for payload in selected.payloads] == ["/erp/orders"]
