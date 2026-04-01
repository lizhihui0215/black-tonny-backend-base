from typing import cast

from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.sales_order import SalesOrder
from ..schemas.sales import SalesOrderCreate, SalesOrderRead, SalesOrderReadListResponse, SalesOrderUpdate

CRUDSalesOrder = FastCRUD[
    SalesOrder,
    SalesOrderCreate,
    SalesOrderUpdate,
    SalesOrderUpdate,
    SalesOrderUpdate,
    SalesOrderRead,
]
crud_sales_orders = CRUDSalesOrder(SalesOrder)


async def get_sales_order_read(
    db: AsyncSession,
    *,
    id: int,
) -> SalesOrderRead | None:
    return await crud_sales_orders.get(
        db=db,
        id=id,
        schema_to_select=SalesOrderRead,
        return_as_model=True,
    )


async def list_sales_order_reads(
    db: AsyncSession,
    *,
    analysis_batch_id: str | None = None,
    order_id: str | None = None,
    offset: int = 0,
    limit: int | None = 100,
) -> SalesOrderReadListResponse:
    filters: dict[str, object] = {}
    if analysis_batch_id is not None:
        filters["analysis_batch_id"] = analysis_batch_id
    if order_id is not None:
        filters["order_id"] = order_id

    response = await crud_sales_orders.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        schema_to_select=SalesOrderRead,
        sort_columns="id",
        sort_orders="asc",
        return_as_model=True,
        return_total_count=True,
        **filters,
    )

    return cast(
        SalesOrderReadListResponse,
        {
            "data": response["data"],
            "total_count": response["total_count"],
        },
    )
