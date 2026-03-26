import asyncio
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import CaptureBase
from src.app.crud.crud_capture_batches import crud_capture_batches
from src.app.crud.crud_capture_endpoint_payloads import crud_capture_endpoint_payloads
from src.app.models.capture_batch import CaptureBatch  # noqa: F401
from src.app.models.capture_endpoint_payload import CaptureEndpointPayload  # noqa: F401
from src.app.schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureBatchUpdate,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
)


def normalize(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return dict(value)


def as_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


@pytest_asyncio.fixture
async def capture_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "capture_contract.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection: Any, _connection_record: Any) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as connection:
        await connection.run_sync(CaptureBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_capture_formal_crud_can_create_batch_and_payload(capture_db_session: AsyncSession) -> None:
    pulled_at = datetime.now(UTC)

    created_batch = await crud_capture_batches.create(
        db=capture_db_session,
        object=CaptureBatchCreate(
            capture_batch_id="batch-001",
            batch_status="queued",
            source_name="erp-report",
            pulled_at=pulled_at,
        ),
        schema_to_select=CaptureBatchRead,
    )
    batch_data = normalize(created_batch)

    created_payload = await crud_capture_endpoint_payloads.create(
        db=capture_db_session,
        object=CaptureEndpointPayloadCreate(
            capture_batch_id="batch-001",
            source_endpoint="/erp/report",
            route_kind="mainline_fact",
            page_cursor="cursor-1",
            page_no=1,
            request_params='{"page":1}',
            payload_json='{"rows":[1]}',
            checksum="checksum-001",
            pulled_at=pulled_at,
        ),
        schema_to_select=CaptureEndpointPayloadRead,
    )
    payload_data = normalize(created_payload)

    fetched_batch = normalize(
        await crud_capture_batches.get(
            db=capture_db_session,
            capture_batch_id="batch-001",
            schema_to_select=CaptureBatchRead,
        )
    )
    fetched_payload = normalize(
        await crud_capture_endpoint_payloads.get(
            db=capture_db_session,
            id=payload_data["id"],
            schema_to_select=CaptureEndpointPayloadRead,
        )
    )

    assert batch_data["capture_batch_id"] == "batch-001"
    assert batch_data["batch_status"] == "queued"
    assert fetched_batch["source_name"] == "erp-report"

    assert payload_data["capture_batch_id"] == "batch-001"
    assert payload_data["source_endpoint"] == "/erp/report"
    assert fetched_payload["checksum"] == "checksum-001"
    assert fetched_payload["page_no"] == 1


@pytest.mark.asyncio
async def test_capture_batch_update_refreshes_updated_at(capture_db_session: AsyncSession) -> None:
    created_batch = normalize(
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id="batch-002",
                batch_status="queued",
                source_name="erp-report",
            ),
            schema_to_select=CaptureBatchRead,
        )
    )

    initial_updated_at = as_datetime(created_batch["updated_at"])
    await asyncio.sleep(0.01)

    await crud_capture_batches.update(
        db=capture_db_session,
        object=CaptureBatchUpdate(batch_status="captured"),
        capture_batch_id="batch-002",
    )
    updated_batch = normalize(
        await crud_capture_batches.get(
            db=capture_db_session,
            capture_batch_id="batch-002",
            schema_to_select=CaptureBatchRead,
        )
    )

    refreshed_updated_at = as_datetime(updated_batch["updated_at"])

    assert updated_batch["batch_status"] == "captured"
    assert refreshed_updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_capture_payload_write_rejects_missing_batch(capture_db_session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        await crud_capture_endpoint_payloads.create(
            db=capture_db_session,
            object=CaptureEndpointPayloadCreate(
                capture_batch_id="missing-batch",
                source_endpoint="/erp/report",
                payload_json='{"rows":[1]}',
                checksum="checksum-missing",
                pulled_at=datetime.now(UTC),
            ),
            schema_to_select=CaptureEndpointPayloadRead,
        )

    await capture_db_session.rollback()
