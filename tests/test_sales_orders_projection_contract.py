import asyncio
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.db.database import ServingBase
from src.app.crud.crud_sales_orders import crud_sales_orders, get_sales_order_read_by_projection_key
from src.app.schemas.sales import (
    SalesOrderCreate,
    SalesOrderProjectionFact,
    SalesOrderRead,
)
from src.app.services.sales_orders_projection_contract import apply_sales_orders_projection_contract


def as_naive_utc(value: datetime) -> datetime:
    return value.astimezone(UTC).replace(tzinfo=None) if value.tzinfo is not None else value


@pytest_asyncio.fixture
async def serving_db_session(tmp_path: Path) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "sales_orders_projection_contract.sqlite3"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)

    async with engine.begin() as connection:
        await connection.run_sync(ServingBase.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_sales_orders_projection_contract_inserts_one_first_slice_row(
    serving_db_session: AsyncSession,
) -> None:
    result = await apply_sales_orders_projection_contract(
        serving_db_session,
        facts=[
            SalesOrderProjectionFact(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-001",
                store_id="store-001",
                order_id="order-001",
                paid_at=datetime(2026, 4, 12, tzinfo=UTC),
                paid_amount=Decimal("88.50"),
                payment_status="paid",
            )
        ],
    )
    stored_row = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )

    assert result.slice_name == "sales_orders"
    assert result.applied_count == 1
    assert result.inserted_count == 1
    assert result.updated_count == 0
    assert stored_row is not None
    assert stored_row.capture_batch_id == "capture-001"
    assert stored_row.store_id == "store-001"
    assert stored_row.paid_amount == Decimal("88.50")
    assert stored_row.payment_status == "paid"


@pytest.mark.asyncio
async def test_sales_orders_projection_contract_updates_existing_row_by_upsert_key(
    serving_db_session: AsyncSession,
) -> None:
    first_result = await apply_sales_orders_projection_contract(
        serving_db_session,
        facts=[
            SalesOrderProjectionFact(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-001",
                store_id="store-001",
                order_id="order-001",
                paid_at=datetime(2026, 4, 12, tzinfo=UTC),
                paid_amount=Decimal("88.50"),
                payment_status="paid",
            )
        ],
    )
    first_row = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )

    assert first_result.inserted_count == 1
    assert first_row is not None
    await asyncio.sleep(0.01)

    second_result = await apply_sales_orders_projection_contract(
        serving_db_session,
        facts=[
            SalesOrderProjectionFact(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-002",
                store_id="store-002",
                order_id="order-001",
                paid_at=datetime(2026, 4, 13, tzinfo=UTC),
                paid_amount=Decimal("99.90"),
                payment_status="refunded",
            )
        ],
    )
    updated_row = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )

    assert second_result.applied_count == 1
    assert second_result.inserted_count == 0
    assert second_result.updated_count == 1
    assert updated_row is not None
    assert updated_row.id == first_row.id
    assert updated_row.created_at == first_row.created_at
    assert updated_row.capture_batch_id == "capture-002"
    assert updated_row.store_id == "store-002"
    assert updated_row.paid_amount == Decimal("99.90")
    assert updated_row.payment_status == "refunded"
    assert updated_row.updated_at > first_row.updated_at


@pytest.mark.asyncio
async def test_sales_orders_projection_contract_dedupes_duplicate_input_keys_with_last_write_wins(
    serving_db_session: AsyncSession,
) -> None:
    result = await apply_sales_orders_projection_contract(
        serving_db_session,
        facts=[
            SalesOrderProjectionFact(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-001",
                store_id="store-001",
                order_id="order-001",
                paid_at=datetime(2026, 4, 12, tzinfo=UTC),
                paid_amount=Decimal("88.50"),
                payment_status="paid",
            ),
            SalesOrderProjectionFact(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-002",
                store_id="store-002",
                order_id="order-001",
                paid_at=datetime(2026, 4, 13, tzinfo=UTC),
                paid_amount=Decimal("98.00"),
                payment_status="partial_refund",
            ),
        ],
    )
    stored_row = await get_sales_order_read_by_projection_key(
        db=serving_db_session,
        analysis_batch_id="analysis-001",
        order_id="order-001",
    )

    assert result.applied_count == 1
    assert result.inserted_count == 1
    assert result.updated_count == 0
    assert stored_row is not None
    assert stored_row.capture_batch_id == "capture-002"
    assert stored_row.store_id == "store-002"
    assert stored_row.paid_amount == Decimal("98.00")
    assert stored_row.payment_status == "partial_refund"
    assert stored_row.paid_at == as_naive_utc(datetime(2026, 4, 13, tzinfo=UTC))


@pytest.mark.asyncio
async def test_sales_orders_projection_contract_persistence_key_rejects_duplicate_rows(
    serving_db_session: AsyncSession,
) -> None:
    await crud_sales_orders.create(
        db=serving_db_session,
        object=SalesOrderCreate(
            analysis_batch_id="analysis-001",
            capture_batch_id="capture-001",
            store_id="store-001",
            order_id="order-001",
            paid_at=datetime(2026, 4, 12, tzinfo=UTC),
            paid_amount=Decimal("88.50"),
            payment_status="paid",
        ),
        schema_to_select=SalesOrderRead,
    )

    with pytest.raises(IntegrityError):
        await crud_sales_orders.create(
            db=serving_db_session,
            object=SalesOrderCreate(
                analysis_batch_id="analysis-001",
                capture_batch_id="capture-002",
                store_id="store-002",
                order_id="order-001",
                paid_at=datetime(2026, 4, 13, tzinfo=UTC),
                paid_amount=Decimal("98.00"),
                payment_status="paid",
            ),
            schema_to_select=SalesOrderRead,
        )

    await serving_db_session.rollback()


def test_sales_orders_projection_fact_requires_contract_fields() -> None:
    schema = SalesOrderProjectionFact.model_json_schema()

    assert {
        "analysis_batch_id",
        "capture_batch_id",
        "order_id",
        "paid_at",
        "paid_amount",
        "payment_status",
    }.issubset(set(schema["required"]))
    assert "store_id" not in schema["required"]
