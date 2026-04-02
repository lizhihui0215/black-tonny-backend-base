from collections.abc import Sequence
from typing import Final, Literal

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.crud_sales_orders import crud_sales_orders, get_sales_order_read_by_projection_key
from ..schemas.sales import (
    SalesOrderCreate,
    SalesOrderProjectionContractResult,
    SalesOrderProjectionFact,
    SalesOrderRead,
    SalesOrderUpdate,
)

_SALES_ORDERS_SLICE_NAME: Final[Literal["sales_orders"]] = "sales_orders"


def _projection_key(fact: SalesOrderProjectionFact) -> tuple[str, str]:
    return (fact.analysis_batch_id, fact.order_id)


def _dedupe_projection_facts(
    facts: Sequence[SalesOrderProjectionFact],
) -> list[SalesOrderProjectionFact]:
    deduped_by_key: dict[tuple[str, str], SalesOrderProjectionFact] = {}

    for fact in facts:
        key = _projection_key(fact)
        if key in deduped_by_key:
            deduped_by_key.pop(key)
        deduped_by_key[key] = fact

    return list(deduped_by_key.values())


async def apply_sales_orders_projection_contract(
    db: AsyncSession,
    *,
    facts: Sequence[SalesOrderProjectionFact],
) -> SalesOrderProjectionContractResult:
    inserted_count = 0
    updated_count = 0
    deduped_facts = _dedupe_projection_facts(facts)

    try:
        for fact in deduped_facts:
            existing_row = await get_sales_order_read_by_projection_key(
                db=db,
                analysis_batch_id=fact.analysis_batch_id,
                order_id=fact.order_id,
            )
            if existing_row is None:
                await crud_sales_orders.create(
                    db=db,
                    object=SalesOrderCreate(
                        analysis_batch_id=fact.analysis_batch_id,
                        capture_batch_id=fact.capture_batch_id,
                        store_id=fact.store_id,
                        order_id=fact.order_id,
                        paid_at=fact.paid_at,
                        paid_amount=fact.paid_amount,
                        payment_status=fact.payment_status,
                    ),
                    commit=False,
                    schema_to_select=SalesOrderRead,
                )
                inserted_count += 1
                continue

            await crud_sales_orders.update(
                db=db,
                object=SalesOrderUpdate(
                    capture_batch_id=fact.capture_batch_id,
                    store_id=fact.store_id,
                    paid_at=fact.paid_at,
                    paid_amount=fact.paid_amount,
                    payment_status=fact.payment_status,
                ),
                id=existing_row.id,
                commit=False,
            )
            updated_count += 1
    except Exception:
        await db.rollback()
        raise

    await db.commit()

    return SalesOrderProjectionContractResult(
        slice_name=_SALES_ORDERS_SLICE_NAME,
        applied_count=len(deduped_facts),
        inserted_count=inserted_count,
        updated_count=updated_count,
    )
