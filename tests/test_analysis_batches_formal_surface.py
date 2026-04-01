import asyncio
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import CaptureBase
from src.app.crud.crud_analysis_batches import (
    crud_analysis_batches,
    get_analysis_batch_read,
    list_analysis_batch_reads,
)
from src.app.models.analysis_batch import AnalysisBatch
from src.app.schemas.analysis import AnalysisBatchCreate, AnalysisBatchRead, AnalysisBatchUpdate


def normalize(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return dict(value)


@pytest_asyncio.fixture
async def capture_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "analysis_batches_boundary.sqlite3"
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
async def test_analysis_batch_formal_crud_can_create_read_and_update(capture_db_session: AsyncSession) -> None:
    created_batch = await crud_analysis_batches.create(
        db=capture_db_session,
        object=AnalysisBatchCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            batch_status="queued",
            source_endpoint="/erp/report",
        ),
        schema_to_select=AnalysisBatchRead,
    )
    created_data = normalize(created_batch)
    fetched_batch = await get_analysis_batch_read(
        db=capture_db_session,
        analysis_batch_id="analysis-001",
    )

    assert created_data["analysis_batch_id"] == "analysis-001"
    assert created_data["batch_status"] == "queued"
    assert created_data["capture_batch_id"] == "capture-001"
    assert fetched_batch is not None
    assert fetched_batch.analysis_batch_id == "analysis-001"
    assert fetched_batch.source_endpoint == "/erp/report"

    initial_updated_at = fetched_batch.updated_at
    await asyncio.sleep(0.01)

    await crud_analysis_batches.update(
        db=capture_db_session,
        object=AnalysisBatchUpdate(
            batch_status="transformed",
            transformed_at=datetime.now(UTC),
        ),
        analysis_batch_id="analysis-001",
    )

    updated_batch = await get_analysis_batch_read(
        db=capture_db_session,
        analysis_batch_id="analysis-001",
    )
    assert updated_batch is not None
    assert updated_batch.batch_status == "transformed"
    assert updated_batch.transformed_at is not None
    assert updated_batch.updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_analysis_batch_list_reads_keep_filters_pagination_and_empty_shape(
    capture_db_session: AsyncSession,
) -> None:
    for analysis_batch_id, capture_batch_id, batch_status in [
        ("analysis-001", "capture-001", "queued"),
        ("analysis-002", "capture-001", "queued"),
        ("analysis-003", "capture-002", "transformed"),
    ]:
        await crud_analysis_batches.create(
            db=capture_db_session,
            object=AnalysisBatchCreate(
                analysis_batch_id=analysis_batch_id,
                capture_batch_id=capture_batch_id,
                batch_status=batch_status,
            ),
            schema_to_select=AnalysisBatchRead,
        )

    filtered_response = await list_analysis_batch_reads(
        db=capture_db_session,
        batch_status="queued",
        capture_batch_id="capture-001",
    )
    paginated_response = await list_analysis_batch_reads(
        db=capture_db_session,
        batch_status="queued",
        offset=1,
        limit=1,
    )
    combined_paginated_response = await list_analysis_batch_reads(
        db=capture_db_session,
        batch_status="queued",
        capture_batch_id="capture-001",
        offset=1,
        limit=1,
    )
    empty_response = await list_analysis_batch_reads(
        db=capture_db_session,
        capture_batch_id="missing-capture",
    )

    assert [row.analysis_batch_id for row in filtered_response["data"]] == ["analysis-001", "analysis-002"]
    assert filtered_response["total_count"] == 2

    assert [row.analysis_batch_id for row in paginated_response["data"]] == ["analysis-002"]
    assert paginated_response["total_count"] == 2

    assert [row.analysis_batch_id for row in combined_paginated_response["data"]] == ["analysis-002"]
    assert combined_paginated_response["total_count"] == 2

    assert empty_response["data"] == []
    assert empty_response["total_count"] == 0


def test_analysis_batch_formal_surface_defaults_and_lengths_stay_minimal() -> None:
    schema_properties = AnalysisBatchCreate.model_json_schema()["properties"]

    assert AnalysisBatchCreate.model_fields["batch_status"].default == "queued"
    assert AnalysisBatch.__table__.c.batch_status.default.arg == "queued"
    assert AnalysisBatch.__table__.c.capture_batch_id.nullable is True
    assert AnalysisBatch.__table__.c.analysis_batch_id.type.length == 64
    assert schema_properties["analysis_batch_id"]["maxLength"] == 64
    assert schema_properties["capture_batch_id"]["anyOf"][0]["maxLength"] == 64
    assert schema_properties["batch_status"]["maxLength"] == 32
    assert schema_properties["source_endpoint"]["anyOf"][0]["maxLength"] == 128
