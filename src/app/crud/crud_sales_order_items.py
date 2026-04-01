from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.sales_order_item import SalesOrderItem
from ..schemas.sales import (
    SalesOrderItemCreate,
    SalesOrderItemRead,
    SalesOrderItemReadListResponse,
    SalesOrderItemUpdate,
)

CRUDSalesOrderItem = FastCRUD[
    SalesOrderItem,
    SalesOrderItemCreate,
    SalesOrderItemUpdate,
    SalesOrderItemUpdate,
    SalesOrderItemUpdate,
    SalesOrderItemRead,
]
crud_sales_order_items = CRUDSalesOrderItem(SalesOrderItem)


async def get_sales_order_item_read(
    db: AsyncSession,
    *,
    id: int,
) -> SalesOrderItemRead | None:
    return await crud_sales_order_items.get(
        db=db,
        id=id,
        schema_to_select=SalesOrderItemRead,
        return_as_model=True,
    )


async def list_sales_order_item_reads(
    db: AsyncSession,
    *,
    analysis_batch_id: str | None = None,
    order_id: str | None = None,
    sku_id: str | None = None,
    offset: int = 0,
    limit: int | None = 100,
) -> SalesOrderItemReadListResponse:
    filters: dict[str, object] = {}
    if analysis_batch_id is not None:
        filters["analysis_batch_id"] = analysis_batch_id
    if order_id is not None:
        filters["order_id"] = order_id
    if sku_id is not None:
        filters["sku_id"] = sku_id

    response = await crud_sales_order_items.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=SalesOrderItemRead,
        sort_columns="id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        SalesOrderItemReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
