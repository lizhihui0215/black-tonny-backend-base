from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.inventory_current import InventoryCurrent
from ..schemas.inventory import (
    InventoryCurrentCreate,
    InventoryCurrentRead,
    InventoryCurrentReadListResponse,
    InventoryCurrentUpdate,
)

CRUDInventoryCurrent = FastCRUD[
    InventoryCurrent,
    InventoryCurrentCreate,
    InventoryCurrentUpdate,
    InventoryCurrentUpdate,
    InventoryCurrentUpdate,
    InventoryCurrentRead,
]
crud_inventory_current = CRUDInventoryCurrent(InventoryCurrent)


async def get_inventory_current_read(
    db: AsyncSession,
    *,
    id: int,
) -> InventoryCurrentRead | None:
    return await crud_inventory_current.get(
        db=db,
        id=id,
        schema_to_select=InventoryCurrentRead,
        return_as_model=True,
    )


async def list_inventory_current_reads(
    db: AsyncSession,
    *,
    analysis_batch_id: str | None = None,
    store_id: str | None = None,
    sku_id: str | None = None,
    offset: int = 0,
    limit: int | None = 100,
) -> InventoryCurrentReadListResponse:
    filters: dict[str, object] = {}
    if analysis_batch_id is not None:
        filters["analysis_batch_id"] = analysis_batch_id
    if store_id is not None:
        filters["store_id"] = store_id
    if sku_id is not None:
        filters["sku_id"] = sku_id

    response = await crud_inventory_current.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=InventoryCurrentRead,
        sort_columns="id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        InventoryCurrentReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
