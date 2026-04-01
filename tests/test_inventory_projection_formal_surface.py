import asyncio
from collections.abc import AsyncGenerator
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import ServingBase
from src.app.crud.crud_inventory_current import (
    crud_inventory_current,
    get_inventory_current_read,
    list_inventory_current_reads,
)
from src.app.crud.crud_inventory_daily_snapshots import (
    crud_inventory_daily_snapshots,
    get_inventory_daily_snapshot_read,
    list_inventory_daily_snapshot_reads,
)
from src.app.models.inventory_current import InventoryCurrent
from src.app.models.inventory_daily_snapshot import InventoryDailySnapshot
from src.app.schemas.inventory import (
    InventoryCurrentCreate,
    InventoryCurrentRead,
    InventoryCurrentUpdate,
    InventoryDailySnapshotCreate,
    InventoryDailySnapshotRead,
    InventoryDailySnapshotUpdate,
)


def normalize(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return dict(value)


@pytest_asyncio.fixture
async def serving_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "inventory_projection_boundary.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    async with engine.begin() as connection:
        await connection.run_sync(ServingBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_inventory_current_formal_crud_can_create_read_and_update(serving_db_session: AsyncSession) -> None:
    created_row = await crud_inventory_current.create(
        db=serving_db_session,
        object=InventoryCurrentCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            store_id="store-001",
            sku_id="sku-001",
            on_hand_qty=Decimal("12.00"),
            safe_stock_qty=Decimal("4.00"),
            is_target_size=True,
        ),
        schema_to_select=InventoryCurrentRead,
    )
    created_data = normalize(created_row)
    fetched_row = await get_inventory_current_read(db=serving_db_session, id=created_data["id"])

    assert created_data["analysis_batch_id"] == "analysis-001"
    assert created_data["on_hand_qty"] == Decimal("12.00")
    assert fetched_row is not None
    assert fetched_row.sku_id == "sku-001"
    assert fetched_row.is_target_size is True

    initial_updated_at = fetched_row.updated_at
    await asyncio.sleep(0.01)

    await crud_inventory_current.update(
        db=serving_db_session,
        object=InventoryCurrentUpdate(
            on_hand_qty=Decimal("10.00"),
            season_tag="carry-over",
        ),
        id=created_data["id"],
    )

    updated_row = await get_inventory_current_read(db=serving_db_session, id=created_data["id"])
    assert updated_row is not None
    assert updated_row.on_hand_qty == Decimal("10.00")
    assert updated_row.season_tag == "carry-over"
    assert updated_row.updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_inventory_current_list_reads_keep_filters_pagination_and_empty_shape(
    serving_db_session: AsyncSession,
) -> None:
    for analysis_batch_id, store_id, sku_id in [
        ("analysis-001", "store-001", "sku-001"),
        ("analysis-001", "store-001", "sku-002"),
        ("analysis-002", "store-002", "sku-003"),
    ]:
        await crud_inventory_current.create(
            db=serving_db_session,
            object=InventoryCurrentCreate(
                analysis_batch_id=analysis_batch_id,
                store_id=store_id,
                sku_id=sku_id,
                on_hand_qty=Decimal("5.00"),
                safe_stock_qty=Decimal("2.00"),
            ),
            schema_to_select=InventoryCurrentRead,
        )

    filtered_response = await list_inventory_current_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        store_id="store-001",
    )
    paginated_response = await list_inventory_current_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        offset=1,
        limit=1,
    )
    empty_response = await list_inventory_current_reads(
        db=serving_db_session,
        sku_id="missing-sku",
    )

    assert [row.sku_id for row in filtered_response["data"]] == ["sku-001", "sku-002"]
    assert filtered_response["total_count"] == 2
    assert [row.sku_id for row in paginated_response["data"]] == ["sku-002"]
    assert paginated_response["total_count"] == 2
    assert empty_response["data"] == []
    assert empty_response["total_count"] == 0


@pytest.mark.asyncio
async def test_inventory_daily_snapshot_formal_crud_can_create_read_and_update(
    serving_db_session: AsyncSession,
) -> None:
    created_row = await crud_inventory_daily_snapshots.create(
        db=serving_db_session,
        object=InventoryDailySnapshotCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            snapshot_date=date(2026, 4, 1),
            store_id="store-001",
            sku_id="sku-001",
            on_hand_qty=Decimal("8.00"),
            safe_stock_qty=Decimal("3.00"),
            is_active_sale=False,
        ),
        schema_to_select=InventoryDailySnapshotRead,
    )
    created_data = normalize(created_row)
    fetched_row = await get_inventory_daily_snapshot_read(db=serving_db_session, id=created_data["id"])

    assert created_data["snapshot_date"] == date(2026, 4, 1)
    assert created_data["safe_stock_qty"] == Decimal("3.00")
    assert fetched_row is not None
    assert fetched_row.sku_id == "sku-001"
    assert fetched_row.is_active_sale is False

    await crud_inventory_daily_snapshots.update(
        db=serving_db_session,
        object=InventoryDailySnapshotUpdate(
            on_hand_qty=Decimal("7.00"),
            season_tag="spring",
        ),
        id=created_data["id"],
    )

    updated_row = await get_inventory_daily_snapshot_read(db=serving_db_session, id=created_data["id"])
    assert updated_row is not None
    assert updated_row.on_hand_qty == Decimal("7.00")
    assert updated_row.season_tag == "spring"


@pytest.mark.asyncio
async def test_inventory_daily_snapshot_list_reads_keep_filters_pagination_and_empty_shape(
    serving_db_session: AsyncSession,
) -> None:
    for analysis_batch_id, snapshot_date_value, sku_id in [
        ("analysis-001", date(2026, 4, 1), "sku-001"),
        ("analysis-001", date(2026, 4, 1), "sku-002"),
        ("analysis-002", date(2026, 4, 2), "sku-003"),
    ]:
        await crud_inventory_daily_snapshots.create(
            db=serving_db_session,
            object=InventoryDailySnapshotCreate(
                analysis_batch_id=analysis_batch_id,
                snapshot_date=snapshot_date_value,
                sku_id=sku_id,
                on_hand_qty=Decimal("6.00"),
                safe_stock_qty=Decimal("2.00"),
            ),
            schema_to_select=InventoryDailySnapshotRead,
        )

    filtered_response = await list_inventory_daily_snapshot_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        snapshot_date=date(2026, 4, 1),
    )
    paginated_response = await list_inventory_daily_snapshot_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        offset=1,
        limit=1,
    )
    empty_response = await list_inventory_daily_snapshot_reads(
        db=serving_db_session,
        sku_id="missing-sku",
    )

    assert [row.sku_id for row in filtered_response["data"]] == ["sku-001", "sku-002"]
    assert filtered_response["total_count"] == 2
    assert [row.sku_id for row in paginated_response["data"]] == ["sku-002"]
    assert paginated_response["total_count"] == 2
    assert empty_response["data"] == []
    assert empty_response["total_count"] == 0


def test_inventory_projection_formal_surface_defaults_and_lengths_stay_minimal() -> None:
    current_properties = InventoryCurrentCreate.model_json_schema()["properties"]
    snapshot_properties = InventoryDailySnapshotCreate.model_json_schema()["properties"]

    assert InventoryCurrentCreate.model_fields["on_hand_qty"].annotation is Decimal
    assert InventoryCurrent.__table__.c.capture_batch_id.nullable is True
    assert InventoryCurrent.__table__.c.store_id.nullable is True
    assert InventoryCurrent.__table__.c.is_all_season.nullable is True
    assert InventoryCurrent.__table__.c.sku_id.type.length == 64
    assert InventoryCurrent.__table__.c.on_hand_qty.type.precision == 18
    assert InventoryCurrent.__table__.c.on_hand_qty.type.scale == 2
    assert current_properties["analysis_batch_id"]["maxLength"] == 64
    assert current_properties["capture_batch_id"]["anyOf"][0]["maxLength"] == 64
    assert current_properties["store_id"]["anyOf"][0]["maxLength"] == 64
    assert current_properties["sku_id"]["maxLength"] == 64
    assert current_properties["on_hand_qty"]["anyOf"][0]["type"] == "number"
    assert current_properties["safe_stock_qty"]["anyOf"][1]["type"] == "string"
    assert current_properties["season_tag"]["anyOf"][0]["maxLength"] == 32

    assert InventoryDailySnapshot.__table__.c.capture_batch_id.nullable is True
    assert InventoryDailySnapshot.__table__.c.store_id.nullable is True
    assert InventoryDailySnapshot.__table__.c.is_target_size.nullable is True
    assert InventoryDailySnapshot.__table__.c.sku_id.type.length == 64
    assert InventoryDailySnapshot.__table__.c.safe_stock_qty.type.precision == 18
    assert InventoryDailySnapshot.__table__.c.safe_stock_qty.type.scale == 2
    assert snapshot_properties["analysis_batch_id"]["maxLength"] == 64
    assert snapshot_properties["capture_batch_id"]["anyOf"][0]["maxLength"] == 64
    assert snapshot_properties["store_id"]["anyOf"][0]["maxLength"] == 64
    assert snapshot_properties["sku_id"]["maxLength"] == 64
    assert snapshot_properties["on_hand_qty"]["anyOf"][1]["type"] == "string"
    assert snapshot_properties["season_tag"]["anyOf"][0]["maxLength"] == 32
