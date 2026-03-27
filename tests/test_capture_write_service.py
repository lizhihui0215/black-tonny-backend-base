import asyncio
import json
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import CaptureBase
from src.app.schemas.capture import CaptureBatchRead, CaptureBatchUpdate, CaptureEndpointPayloadRead
from src.app.services.capture_write import (
    append_capture_payload,
    create_capture_batch,
    update_capture_batch,
)


def dump_json(value: Any) -> str:
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
    db_path = tmp_path / "capture_write_service.sqlite3"
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
async def test_create_capture_batch_generates_id_and_uses_explicit_source_name(
    capture_db_session: AsyncSession,
) -> None:
    created_batch = await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
    )

    assert isinstance(created_batch, CaptureBatchRead)
    assert len(created_batch.capture_batch_id) == 32
    assert created_batch.batch_status == "queued"
    assert created_batch.source_name == "yeusoft.capture"


@pytest.mark.asyncio
async def test_create_capture_batch_preserves_explicit_capture_batch_id(
    capture_db_session: AsyncSession,
) -> None:
    created_batch = await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
        capture_batch_id="batch-explicit-001",
    )

    assert created_batch.capture_batch_id == "batch-explicit-001"


@pytest.mark.asyncio
async def test_update_capture_batch_applies_capture_batch_update_contract(
    capture_db_session: AsyncSession,
) -> None:
    created_batch = await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
        capture_batch_id="batch-update-001",
    )
    initial_updated_at = created_batch.updated_at
    pulled_at = datetime.now(UTC)

    await asyncio.sleep(0.01)

    updated_batch = await update_capture_batch(
        db=capture_db_session,
        capture_batch_id="batch-update-001",
        values=CaptureBatchUpdate(
            batch_status="captured",
            pulled_at=pulled_at,
            error_message="captured successfully",
        ),
    )

    assert isinstance(updated_batch, CaptureBatchRead)
    assert updated_batch.batch_status == "captured"
    assert updated_batch.pulled_at == as_naive_utc(pulled_at)
    assert updated_batch.error_message == "captured successfully"
    assert updated_batch.updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_update_capture_batch_returns_none_for_missing_batch(
    capture_db_session: AsyncSession,
) -> None:
    updated_batch = await update_capture_batch(
        db=capture_db_session,
        capture_batch_id="missing-batch",
        values=CaptureBatchUpdate(batch_status="failed"),
    )

    assert updated_batch is None


@pytest.mark.asyncio
async def test_append_capture_payload_serializes_with_stable_json_and_checksum(
    capture_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
        capture_batch_id="batch-payload-001",
    )
    pulled_at = datetime.now(UTC)
    payload = {"b": 2, "a": [{"nested": True}, 1]}
    request_params = {"page": 2, "filters": {"keyword": "连衣裙", "enabled": True}}
    expected_payload_json = dump_json(payload)
    expected_request_params_json = dump_json(request_params)
    expected_checksum = sha256(expected_payload_json.encode("utf-8")).hexdigest()

    created_payload = await append_capture_payload(
        db=capture_db_session,
        capture_batch_id="batch-payload-001",
        source_endpoint="/erp/report",
        payload=payload,
        request_params=request_params,
        route_kind="document",
        page_cursor="cursor-2",
        page_no=2,
        pulled_at=pulled_at,
    )

    assert isinstance(created_payload, CaptureEndpointPayloadRead)
    assert created_payload.payload_json == expected_payload_json
    assert created_payload.request_params == expected_request_params_json
    assert created_payload.checksum == expected_checksum
    assert created_payload.pulled_at == as_naive_utc(pulled_at)
    assert created_payload.route_kind == "document"
    assert created_payload.page_cursor == "cursor-2"
    assert created_payload.page_no == 2


@pytest.mark.asyncio
async def test_append_capture_payload_defaults_pulled_at_when_omitted(
    capture_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
        capture_batch_id="batch-payload-002",
    )
    before_append = datetime.now(UTC)

    created_payload = await append_capture_payload(
        db=capture_db_session,
        capture_batch_id="batch-payload-002",
        source_endpoint="/erp/report",
        payload={"items": [1, 2, 3]},
    )
    after_append = datetime.now(UTC)

    assert isinstance(created_payload, CaptureEndpointPayloadRead)
    assert as_naive_utc(before_append) <= created_payload.pulled_at <= as_naive_utc(after_append)


@pytest.mark.asyncio
async def test_append_capture_payload_raises_for_non_json_serializable_payload(
    capture_db_session: AsyncSession,
) -> None:
    await create_capture_batch(
        db=capture_db_session,
        source_name="yeusoft.capture",
        capture_batch_id="batch-payload-003",
    )

    with pytest.raises(TypeError):
        await append_capture_payload(
            db=capture_db_session,
            capture_batch_id="batch-payload-003",
            source_endpoint="/erp/report",
            payload={"invalid": object()},
        )


@pytest.mark.asyncio
async def test_append_capture_payload_preserves_fk_integrity_error_for_missing_batch(
    capture_db_session: AsyncSession,
) -> None:
    with pytest.raises(IntegrityError):
        await append_capture_payload(
            db=capture_db_session,
            capture_batch_id="missing-batch",
            source_endpoint="/erp/report",
            payload={"items": [1, 2, 3]},
        )
