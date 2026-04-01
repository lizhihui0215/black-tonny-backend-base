from datetime import date
from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.inventory_daily_snapshot import InventoryDailySnapshot
from ..schemas.inventory import (
    InventoryDailySnapshotCreate,
    InventoryDailySnapshotRead,
    InventoryDailySnapshotReadListResponse,
    InventoryDailySnapshotUpdate,
)

CRUDInventoryDailySnapshot = FastCRUD[
    InventoryDailySnapshot,
    InventoryDailySnapshotCreate,
    InventoryDailySnapshotUpdate,
    InventoryDailySnapshotUpdate,
    InventoryDailySnapshotUpdate,
    InventoryDailySnapshotRead,
]
crud_inventory_daily_snapshots = CRUDInventoryDailySnapshot(InventoryDailySnapshot)


async def get_inventory_daily_snapshot_read(
    db: AsyncSession,
    *,
    id: int,
) -> InventoryDailySnapshotRead | None:
    return await crud_inventory_daily_snapshots.get(
        db=db,
        id=id,
        schema_to_select=InventoryDailySnapshotRead,
        return_as_model=True,
    )


async def list_inventory_daily_snapshot_reads(
    db: AsyncSession,
    *,
    analysis_batch_id: str | None = None,
    snapshot_date: date | None = None,
    sku_id: str | None = None,
    offset: int = 0,
    limit: int | None = 100,
) -> InventoryDailySnapshotReadListResponse:
    filters: dict[str, object] = {}
    if analysis_batch_id is not None:
        filters["analysis_batch_id"] = analysis_batch_id
    if snapshot_date is not None:
        filters["snapshot_date"] = snapshot_date
    if sku_id is not None:
        filters["sku_id"] = sku_id

    response = await crud_inventory_daily_snapshots.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=InventoryDailySnapshotRead,
        sort_columns="id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        InventoryDailySnapshotReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
