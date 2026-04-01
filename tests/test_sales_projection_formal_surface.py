import asyncio
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import ServingBase
from src.app.crud.crud_sales_order_items import (
    crud_sales_order_items,
    get_sales_order_item_read,
    list_sales_order_item_reads,
)
from src.app.crud.crud_sales_orders import crud_sales_orders, get_sales_order_read, list_sales_order_reads
from src.app.models.sales_order import SalesOrder
from src.app.models.sales_order_item import SalesOrderItem
from src.app.schemas.sales import (
    SalesOrderCreate,
    SalesOrderItemCreate,
    SalesOrderItemRead,
    SalesOrderItemUpdate,
    SalesOrderRead,
    SalesOrderUpdate,
)


def normalize(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return dict(value)


@pytest_asyncio.fixture
async def serving_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "sales_projection_boundary.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    async with engine.begin() as connection:
        await connection.run_sync(ServingBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_sales_order_formal_crud_can_create_read_and_update(serving_db_session: AsyncSession) -> None:
    created_order = await crud_sales_orders.create(
        db=serving_db_session,
        object=SalesOrderCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            store_id="store-001",
            order_id="order-001",
            paid_at=datetime.now(UTC),
            paid_amount=Decimal("188.50"),
        ),
        schema_to_select=SalesOrderRead,
    )
    created_data = normalize(created_order)
    fetched_order = await get_sales_order_read(db=serving_db_session, id=created_data["id"])

    assert created_data["analysis_batch_id"] == "analysis-001"
    assert created_data["paid_amount"] == Decimal("188.50")
    assert created_data["payment_status"] == "paid"
    assert fetched_order is not None
    assert fetched_order.order_id == "order-001"
    assert fetched_order.store_id == "store-001"

    initial_updated_at = fetched_order.updated_at
    await asyncio.sleep(0.01)

    await crud_sales_orders.update(
        db=serving_db_session,
        object=SalesOrderUpdate(
            paid_amount=Decimal("200.00"),
            payment_status="refunded",
        ),
        id=created_data["id"],
    )

    updated_order = await get_sales_order_read(db=serving_db_session, id=created_data["id"])
    assert updated_order is not None
    assert updated_order.paid_amount == Decimal("200.00")
    assert updated_order.payment_status == "refunded"
    assert updated_order.updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_sales_order_list_reads_keep_filters_pagination_and_empty_shape(
    serving_db_session: AsyncSession,
) -> None:
    paid_at = datetime.now(UTC)
    for analysis_batch_id, order_id in [
        ("analysis-001", "order-001"),
        ("analysis-001", "order-002"),
        ("analysis-002", "order-003"),
    ]:
        await crud_sales_orders.create(
            db=serving_db_session,
            object=SalesOrderCreate(
                analysis_batch_id=analysis_batch_id,
                order_id=order_id,
                paid_at=paid_at,
                paid_amount=Decimal("99.00"),
            ),
            schema_to_select=SalesOrderRead,
        )

    filtered_response = await list_sales_order_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
    )
    paginated_response = await list_sales_order_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        offset=1,
        limit=1,
    )
    empty_response = await list_sales_order_reads(
        db=serving_db_session,
        order_id="missing-order",
    )

    assert [row.order_id for row in filtered_response["data"]] == ["order-001", "order-002"]
    assert filtered_response["total_count"] == 2
    assert [row.order_id for row in paginated_response["data"]] == ["order-002"]
    assert paginated_response["total_count"] == 2
    assert empty_response["data"] == []
    assert empty_response["total_count"] == 0


@pytest.mark.asyncio
async def test_sales_order_item_formal_crud_can_create_read_and_update(serving_db_session: AsyncSession) -> None:
    created_item = await crud_sales_order_items.create(
        db=serving_db_session,
        object=SalesOrderItemCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            order_id="order-001",
            sku_id="sku-001",
            style_code="style-001",
            quantity=2,
        ),
        schema_to_select=SalesOrderItemRead,
    )
    created_data = normalize(created_item)
    fetched_item = await get_sales_order_item_read(db=serving_db_session, id=created_data["id"])

    assert created_data["analysis_batch_id"] == "analysis-001"
    assert fetched_item is not None
    assert fetched_item.sku_id == "sku-001"
    assert fetched_item.style_code == "style-001"

    initial_updated_at = fetched_item.updated_at
    await asyncio.sleep(0.01)

    await crud_sales_order_items.update(
        db=serving_db_session,
        object=SalesOrderItemUpdate(
            quantity=3,
            color_code="black",
        ),
        id=created_data["id"],
    )

    updated_item = await get_sales_order_item_read(db=serving_db_session, id=created_data["id"])
    assert updated_item is not None
    assert updated_item.quantity == 3
    assert updated_item.color_code == "black"
    assert updated_item.updated_at > initial_updated_at


@pytest.mark.asyncio
async def test_sales_order_item_list_reads_keep_filters_pagination_and_empty_shape(
    serving_db_session: AsyncSession,
) -> None:
    for analysis_batch_id, order_id, sku_id in [
        ("analysis-001", "order-001", "sku-001"),
        ("analysis-001", "order-001", "sku-002"),
        ("analysis-002", "order-002", "sku-003"),
    ]:
        await crud_sales_order_items.create(
            db=serving_db_session,
            object=SalesOrderItemCreate(
                analysis_batch_id=analysis_batch_id,
                order_id=order_id,
                sku_id=sku_id,
                quantity=1,
            ),
            schema_to_select=SalesOrderItemRead,
        )

    filtered_response = await list_sales_order_item_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )
    paginated_response = await list_sales_order_item_reads(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        offset=1,
        limit=1,
    )
    empty_response = await list_sales_order_item_reads(
        db=serving_db_session,
        sku_id="missing-sku",
    )

    assert [row.sku_id for row in filtered_response["data"]] == ["sku-001", "sku-002"]
    assert filtered_response["total_count"] == 2
    assert [row.sku_id for row in paginated_response["data"]] == ["sku-002"]
    assert paginated_response["total_count"] == 2
    assert empty_response["data"] == []
    assert empty_response["total_count"] == 0


def test_sales_projection_formal_surface_defaults_and_lengths_stay_minimal() -> None:
    order_properties = SalesOrderCreate.model_json_schema()["properties"]
    item_properties = SalesOrderItemCreate.model_json_schema()["properties"]

    assert SalesOrderCreate.model_fields["payment_status"].default == "paid"
    assert SalesOrderCreate.model_fields["paid_amount"].annotation is Decimal
    assert SalesOrder.__table__.c.payment_status.default.arg == "paid"
    assert SalesOrder.__table__.c.paid_amount.default.arg == Decimal("0.00")
    assert SalesOrder.__table__.c.capture_batch_id.nullable is True
    assert SalesOrder.__table__.c.store_id.nullable is True
    assert SalesOrder.__table__.c.order_id.type.length == 64
    assert SalesOrder.__table__.c.paid_amount.type.precision == 18
    assert SalesOrder.__table__.c.paid_amount.type.scale == 2
    assert order_properties["analysis_batch_id"]["maxLength"] == 64
    assert order_properties["capture_batch_id"]["anyOf"][0]["maxLength"] == 64
    assert order_properties["store_id"]["anyOf"][0]["maxLength"] == 64
    assert order_properties["order_id"]["maxLength"] == 64
    assert order_properties["paid_amount"]["anyOf"][0]["type"] == "number"
    assert order_properties["paid_amount"]["anyOf"][1]["type"] == "string"
    assert order_properties["payment_status"]["maxLength"] == 32

    assert SalesOrderItem.__table__.c.capture_batch_id.nullable is True
    assert SalesOrderItem.__table__.c.sku_id.type.length == 64
    assert item_properties["analysis_batch_id"]["maxLength"] == 64
    assert item_properties["capture_batch_id"]["anyOf"][0]["maxLength"] == 64
    assert item_properties["order_id"]["maxLength"] == 64
    assert item_properties["sku_id"]["maxLength"] == 64
    assert item_properties["style_code"]["anyOf"][0]["maxLength"] == 64
    assert item_properties["color_code"]["anyOf"][0]["maxLength"] == 64
    assert item_properties["size_code"]["anyOf"][0]["maxLength"] == 64
