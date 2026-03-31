import asyncio
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from types import FunctionType
from typing import Any

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import event
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.constants.capture import (
    CAPTURE_BATCH_DEFAULT_STATUS,
    CAPTURE_BATCH_ID_MAX_LENGTH,
    CAPTURE_CHECKSUM_MAX_LENGTH,
    CAPTURE_PAGE_CURSOR_MAX_LENGTH,
    CAPTURE_ROUTE_KIND_MAX_LENGTH,
    CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH,
    CAPTURE_SOURCE_NAME_MAX_LENGTH,
)
from src.app.core.db.database import CaptureBase
from src.app.crud.crud_capture_batches import (
    crud_capture_batches,
    get_capture_batch_read,
    list_capture_batch_reads,
)
from src.app.crud.crud_capture_endpoint_payloads import (
    crud_capture_endpoint_payloads,
    get_capture_endpoint_payload_read,
    list_capture_endpoint_payload_reads,
)
from src.app.models.capture_batch import CaptureBatch
from src.app.models.capture_endpoint_payload import CaptureEndpointPayload  # noqa: F401
from src.app.schemas.capture import (
    CaptureBatchCreate,
    CaptureBatchRead,
    CaptureBatchUpdate,
    CaptureEndpointPayloadCreate,
    CaptureEndpointPayloadRead,
    CaptureEndpointPayloadUpdate,
)
from src.app.services import capture_write as capture_write_module


def normalize(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return dict(value)


def as_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def make_large_json_payload(key: str, content_char: str, *, content_length: int) -> str:
    return f'{{"{key}":"{content_char * content_length}"}}'


def extract_string_schema(property_schema: dict[str, Any]) -> dict[str, Any]:
    if property_schema.get("type") == "string":
        return property_schema

    for variant in property_schema.get("anyOf", []):
        if variant.get("type") == "string":
            return variant

    raise AssertionError(f"could not find string schema in {property_schema!r}")


@pytest_asyncio.fixture
async def capture_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "capture_boundary.sqlite3"
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


def test_capture_large_text_columns_compile_to_text_for_postgresql() -> None:
    postgresql_dialect = postgresql.dialect()

    assert CaptureBatch.__table__.c.error_message.type.compile(dialect=postgresql_dialect) == "TEXT"
    assert CaptureEndpointPayload.__table__.c.payload_json.type.compile(dialect=postgresql_dialect) == "TEXT"
    assert CaptureEndpointPayload.__table__.c.request_params.type.compile(dialect=postgresql_dialect) == "TEXT"


def test_capture_large_text_fields_do_not_declare_explicit_max_length_in_formal_schemas() -> None:
    batch_create_schema = CaptureBatchCreate.model_json_schema()["properties"]["error_message"]
    batch_update_schema = CaptureBatchUpdate.model_json_schema()["properties"]["error_message"]
    payload_create_request_schema = CaptureEndpointPayloadCreate.model_json_schema()["properties"]["request_params"]
    payload_create_payload_schema = CaptureEndpointPayloadCreate.model_json_schema()["properties"]["payload_json"]
    payload_update_request_schema = CaptureEndpointPayloadUpdate.model_json_schema()["properties"]["request_params"]
    payload_update_payload_schema = CaptureEndpointPayloadUpdate.model_json_schema()["properties"]["payload_json"]

    assert "maxLength" not in extract_string_schema(batch_create_schema)
    assert "maxLength" not in extract_string_schema(batch_update_schema)
    assert "maxLength" not in extract_string_schema(payload_create_request_schema)
    assert "maxLength" not in extract_string_schema(payload_create_payload_schema)
    assert "maxLength" not in extract_string_schema(payload_update_request_schema)
    assert "maxLength" not in extract_string_schema(payload_update_payload_schema)


def test_capture_minimal_write_helper_surface_exposes_only_documented_entry_points() -> None:
    public_function_names = sorted(
        name
        for name, value in capture_write_module.__dict__.items()
        if isinstance(value, FunctionType)
        and value.__module__ == capture_write_module.__name__
        and not name.startswith("_")
    )

    assert public_function_names == [
        "append_capture_payload",
        "create_capture_batch",
        "update_capture_batch",
    ]


def test_capture_minimal_constants_surface_stays_aligned_with_models_schemas_and_helper_defaults() -> None:
    batch_create_schema = CaptureBatchCreate.model_json_schema()["properties"]
    batch_update_schema = CaptureBatchUpdate.model_json_schema()["properties"]
    payload_create_schema = CaptureEndpointPayloadCreate.model_json_schema()["properties"]
    payload_update_schema = CaptureEndpointPayloadUpdate.model_json_schema()["properties"]

    assert CAPTURE_BATCH_DEFAULT_STATUS == "queued"
    assert CaptureBatchCreate.model_fields["batch_status"].default == CAPTURE_BATCH_DEFAULT_STATUS
    assert CaptureBatch.__table__.c.batch_status.default.arg == CAPTURE_BATCH_DEFAULT_STATUS
    assert capture_write_module.create_capture_batch.__kwdefaults__["batch_status"] == CAPTURE_BATCH_DEFAULT_STATUS

    assert CAPTURE_BATCH_ID_MAX_LENGTH == CaptureBatch.__table__.c.capture_batch_id.type.length
    assert CAPTURE_BATCH_ID_MAX_LENGTH == batch_create_schema["capture_batch_id"]["maxLength"]
    assert CAPTURE_BATCH_ID_MAX_LENGTH == payload_create_schema["capture_batch_id"]["maxLength"]

    assert CAPTURE_SOURCE_NAME_MAX_LENGTH == CaptureBatch.__table__.c.source_name.type.length
    assert CAPTURE_SOURCE_NAME_MAX_LENGTH == batch_create_schema["source_name"]["maxLength"]
    assert CAPTURE_SOURCE_NAME_MAX_LENGTH == extract_string_schema(batch_update_schema["source_name"])["maxLength"]

    assert CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH == CaptureEndpointPayload.__table__.c.source_endpoint.type.length
    assert CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH == payload_create_schema["source_endpoint"]["maxLength"]
    assert (
        CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH
        == extract_string_schema(payload_update_schema["source_endpoint"])["maxLength"]
    )

    assert CAPTURE_ROUTE_KIND_MAX_LENGTH == CaptureEndpointPayload.__table__.c.route_kind.type.length
    assert CAPTURE_ROUTE_KIND_MAX_LENGTH == extract_string_schema(payload_create_schema["route_kind"])["maxLength"]
    assert CAPTURE_ROUTE_KIND_MAX_LENGTH == extract_string_schema(payload_update_schema["route_kind"])["maxLength"]

    assert CAPTURE_PAGE_CURSOR_MAX_LENGTH == CaptureEndpointPayload.__table__.c.page_cursor.type.length
    assert CAPTURE_PAGE_CURSOR_MAX_LENGTH == extract_string_schema(payload_create_schema["page_cursor"])["maxLength"]
    assert CAPTURE_PAGE_CURSOR_MAX_LENGTH == extract_string_schema(payload_update_schema["page_cursor"])["maxLength"]

    assert CAPTURE_CHECKSUM_MAX_LENGTH == CaptureEndpointPayload.__table__.c.checksum.type.length
    assert CAPTURE_CHECKSUM_MAX_LENGTH == payload_create_schema["checksum"]["maxLength"]
    assert CAPTURE_CHECKSUM_MAX_LENGTH == extract_string_schema(payload_update_schema["checksum"])["maxLength"]


@pytest.mark.asyncio
async def test_capture_formal_boundary_accepts_large_text_fields(capture_db_session: AsyncSession) -> None:
    large_error_message = "E" * 70000
    large_request_params = make_large_json_payload("search", "r", content_length=70000)
    large_payload_json = make_large_json_payload("blob", "p", content_length=80000)
    pulled_at = datetime.now(UTC)

    await crud_capture_batches.create(
        db=capture_db_session,
        object=CaptureBatchCreate(
            capture_batch_id="batch-large-text-001",
            batch_status="queued",
            source_name="erp-large-text",
            error_message=large_error_message,
        ),
        schema_to_select=CaptureBatchRead,
    )

    created_payload = normalize(
        await crud_capture_endpoint_payloads.create(
            db=capture_db_session,
            object=CaptureEndpointPayloadCreate(
                capture_batch_id="batch-large-text-001",
                source_endpoint="/erp/large-payload",
                request_params=large_request_params,
                payload_json=large_payload_json,
                checksum="checksum-large-text-001",
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureEndpointPayloadRead,
        )
    )

    persisted_batch = await get_capture_batch_read(
        db=capture_db_session,
        capture_batch_id="batch-large-text-001",
    )
    persisted_payload = await get_capture_endpoint_payload_read(
        db=capture_db_session,
        id=created_payload["id"],
    )

    assert isinstance(persisted_batch, CaptureBatchRead)
    assert isinstance(persisted_payload, CaptureEndpointPayloadRead)
    assert len(persisted_batch.error_message or "") == len(large_error_message)
    assert len(persisted_payload.request_params or "") == len(large_request_params)
    assert len(persisted_payload.payload_json) == len(large_payload_json)


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


def test_capture_batch_update_schema_rejects_updated_at_override() -> None:
    with pytest.raises(ValidationError):
        CaptureBatchUpdate(updated_at=datetime.now(UTC))


@pytest.mark.asyncio
async def test_capture_batch_status_constraint_rejects_unknown_value(capture_db_session: AsyncSession) -> None:
    capture_db_session.add(
        CaptureBatch(
            capture_batch_id="batch-invalid",
            batch_status="unexpected",
            source_name="erp-report",
        )
    )

    with pytest.raises(IntegrityError):
        await capture_db_session.commit()

    await capture_db_session.rollback()


@pytest.mark.asyncio
async def test_capture_batch_read_helpers_return_models_and_stable_list_shape(
    capture_db_session: AsyncSession,
) -> None:
    for capture_batch_id, batch_status in (
        ("batch-010", "queued"),
        ("batch-020", "captured"),
        ("batch-030", "queued"),
    ):
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id=capture_batch_id,
                batch_status=batch_status,
                source_name="erp-report",
            ),
            schema_to_select=CaptureBatchRead,
        )

    batch_read = await get_capture_batch_read(db=capture_db_session, capture_batch_id="batch-020")
    queued_batches = await list_capture_batch_reads(
        db=capture_db_session,
        batch_status="queued",
    )
    missing_batch = await get_capture_batch_read(db=capture_db_session, capture_batch_id="missing-batch")

    assert isinstance(batch_read, CaptureBatchRead)
    assert batch_read.capture_batch_id == "batch-020"
    assert batch_read.batch_status == "captured"

    assert queued_batches["total_count"] == 2
    assert [item.capture_batch_id for item in queued_batches["data"]] == ["batch-010", "batch-030"]
    assert all(isinstance(item, CaptureBatchRead) for item in queued_batches["data"])

    assert missing_batch is None


@pytest.mark.asyncio
async def test_capture_batch_list_read_helper_handles_pagination_and_empty_results(
    capture_db_session: AsyncSession,
) -> None:
    for capture_batch_id in ("batch-110", "batch-120", "batch-130"):
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id=capture_batch_id,
                batch_status="queued",
                source_name="erp-paginated",
            ),
            schema_to_select=CaptureBatchRead,
        )

    paginated_batches = await list_capture_batch_reads(
        db=capture_db_session,
        source_name="erp-paginated",
        offset=1,
        limit=1,
    )
    out_of_range_batches = await list_capture_batch_reads(
        db=capture_db_session,
        source_name="erp-paginated",
        offset=5,
        limit=2,
    )
    empty_batches = await list_capture_batch_reads(
        db=capture_db_session,
        source_name="missing-source",
        offset=0,
        limit=2,
    )

    assert paginated_batches["total_count"] == 3
    assert [item.capture_batch_id for item in paginated_batches["data"]] == ["batch-120"]

    assert out_of_range_batches["total_count"] == 3
    assert out_of_range_batches["data"] == []

    assert empty_batches["total_count"] == 0
    assert empty_batches["data"] == []


@pytest.mark.asyncio
async def test_capture_batch_list_read_helper_handles_combined_filters_with_default_and_explicit_limits(
    capture_db_session: AsyncSession,
) -> None:
    for capture_batch_id, batch_status, source_name in (
        ("batch-410", "queued", "erp-report"),
        ("batch-420", "queued", "erp-report"),
        ("batch-430", "captured", "erp-report"),
        ("batch-440", "queued", "erp-other"),
    ):
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id=capture_batch_id,
                batch_status=batch_status,
                source_name=source_name,
            ),
            schema_to_select=CaptureBatchRead,
        )

    default_limited_batches = await list_capture_batch_reads(
        db=capture_db_session,
        batch_status="queued",
        source_name="erp-report",
    )
    paginated_batches = await list_capture_batch_reads(
        db=capture_db_session,
        batch_status="queued",
        source_name="erp-report",
        offset=1,
        limit=1,
    )
    empty_combined_batches = await list_capture_batch_reads(
        db=capture_db_session,
        batch_status="captured",
        source_name="erp-other",
    )

    assert default_limited_batches["total_count"] == 2
    assert [item.capture_batch_id for item in default_limited_batches["data"]] == ["batch-410", "batch-420"]

    assert paginated_batches["total_count"] == 2
    assert [item.capture_batch_id for item in paginated_batches["data"]] == ["batch-420"]

    assert empty_combined_batches["total_count"] == 0
    assert empty_combined_batches["data"] == []


@pytest.mark.asyncio
async def test_capture_payload_read_helpers_return_models_with_filtered_sorted_results(
    capture_db_session: AsyncSession,
) -> None:
    pulled_at = datetime.now(UTC)
    for capture_batch_id in ("batch-100", "batch-200"):
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id=capture_batch_id,
                batch_status="queued",
                source_name="erp-report",
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureBatchRead,
        )

    payload_ids: list[int] = []
    for capture_batch_id, source_endpoint, checksum in (
        ("batch-100", "/erp/report/a", "checksum-a"),
        ("batch-100", "/erp/report/b", "checksum-b"),
        ("batch-200", "/erp/report/c", "checksum-c"),
    ):
        created_payload = await crud_capture_endpoint_payloads.create(
            db=capture_db_session,
            object=CaptureEndpointPayloadCreate(
                capture_batch_id=capture_batch_id,
                source_endpoint=source_endpoint,
                payload_json='{"rows":[1]}',
                checksum=checksum,
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureEndpointPayloadRead,
        )
        payload_ids.append(normalize(created_payload)["id"])

    payload_read = await get_capture_endpoint_payload_read(db=capture_db_session, id=payload_ids[0])
    batch_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-100",
    )
    filtered_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        source_endpoint="/erp/report/c",
    )
    missing_payload = await get_capture_endpoint_payload_read(db=capture_db_session, id=999999)

    assert isinstance(payload_read, CaptureEndpointPayloadRead)
    assert payload_read.id == payload_ids[0]
    assert payload_read.capture_batch_id == "batch-100"

    assert batch_payloads["total_count"] == 2
    assert [item.id for item in batch_payloads["data"]] == payload_ids[:2]
    assert all(isinstance(item, CaptureEndpointPayloadRead) for item in batch_payloads["data"])

    assert filtered_payloads["total_count"] == 1
    assert filtered_payloads["data"][0].checksum == "checksum-c"

    assert missing_payload is None


@pytest.mark.asyncio
async def test_capture_payload_list_read_helper_handles_pagination_and_empty_results(
    capture_db_session: AsyncSession,
) -> None:
    pulled_at = datetime.now(UTC)
    await crud_capture_batches.create(
        db=capture_db_session,
        object=CaptureBatchCreate(
            capture_batch_id="batch-300",
            batch_status="queued",
            source_name="erp-report",
            pulled_at=pulled_at,
        ),
        schema_to_select=CaptureBatchRead,
    )

    paginated_ids: list[int] = []
    for source_endpoint, checksum in (
        ("/erp/paginated/a", "checksum-pa"),
        ("/erp/paginated/b", "checksum-pb"),
        ("/erp/paginated/c", "checksum-pc"),
    ):
        created_payload = await crud_capture_endpoint_payloads.create(
            db=capture_db_session,
            object=CaptureEndpointPayloadCreate(
                capture_batch_id="batch-300",
                source_endpoint=source_endpoint,
                payload_json='{"rows":[1]}',
                checksum=checksum,
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureEndpointPayloadRead,
        )
        paginated_ids.append(normalize(created_payload)["id"])

    paginated_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-300",
        offset=1,
        limit=1,
    )
    out_of_range_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-300",
        offset=8,
        limit=2,
    )
    empty_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        source_endpoint="/missing-endpoint",
        offset=0,
        limit=2,
    )

    assert paginated_payloads["total_count"] == 3
    assert [item.id for item in paginated_payloads["data"]] == [paginated_ids[1]]

    assert out_of_range_payloads["total_count"] == 3
    assert out_of_range_payloads["data"] == []

    assert empty_payloads["total_count"] == 0
    assert empty_payloads["data"] == []


@pytest.mark.asyncio
async def test_capture_payload_list_read_helper_handles_combined_filters_with_default_and_explicit_limits(
    capture_db_session: AsyncSession,
) -> None:
    pulled_at = datetime.now(UTC)
    for capture_batch_id in ("batch-500", "batch-600"):
        await crud_capture_batches.create(
            db=capture_db_session,
            object=CaptureBatchCreate(
                capture_batch_id=capture_batch_id,
                batch_status="queued",
                source_name="erp-query",
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureBatchRead,
        )

    combined_ids: list[int] = []
    for capture_batch_id, source_endpoint, checksum in (
        ("batch-500", "/erp/query/a", "checksum-qa1"),
        ("batch-500", "/erp/query/a", "checksum-qa2"),
        ("batch-500", "/erp/query/b", "checksum-qb1"),
        ("batch-600", "/erp/query/a", "checksum-qa3"),
    ):
        created_payload = await crud_capture_endpoint_payloads.create(
            db=capture_db_session,
            object=CaptureEndpointPayloadCreate(
                capture_batch_id=capture_batch_id,
                source_endpoint=source_endpoint,
                payload_json='{"rows":[1]}',
                checksum=checksum,
                pulled_at=pulled_at,
            ),
            schema_to_select=CaptureEndpointPayloadRead,
        )
        if capture_batch_id == "batch-500" and source_endpoint == "/erp/query/a":
            combined_ids.append(normalize(created_payload)["id"])

    default_limited_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-500",
        source_endpoint="/erp/query/a",
    )
    paginated_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-500",
        source_endpoint="/erp/query/a",
        offset=1,
        limit=1,
    )
    empty_combined_payloads = await list_capture_endpoint_payload_reads(
        db=capture_db_session,
        capture_batch_id="batch-600",
        source_endpoint="/erp/query/b",
    )

    assert default_limited_payloads["total_count"] == 2
    assert [item.id for item in default_limited_payloads["data"]] == combined_ids

    assert paginated_payloads["total_count"] == 2
    assert [item.id for item in paginated_payloads["data"]] == [combined_ids[1]]

    assert empty_combined_payloads["total_count"] == 0
    assert empty_combined_payloads["data"] == []
