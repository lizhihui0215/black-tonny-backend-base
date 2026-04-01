from typing import Final, Literal

from ..schemas.transform import (
    AdmittedTransformInputSnapshot,
    TransformReadinessDecision,
)

_SALES_ORDERS_SLICE_NAME: Final[Literal["sales_orders"]] = "sales_orders"
_SALES_ORDERS_SOURCE_ENDPOINT: Final[str] = "/erp/orders"


def _count_sales_orders_payloads(admitted_input: AdmittedTransformInputSnapshot) -> int:
    return sum(1 for payload in admitted_input.payloads if payload.source_endpoint == _SALES_ORDERS_SOURCE_ENDPOINT)


def evaluate_sales_orders_transform_readiness(
    admitted_input: AdmittedTransformInputSnapshot,
) -> TransformReadinessDecision:
    matched_payload_count = _count_sales_orders_payloads(admitted_input)

    if matched_payload_count == 0:
        return TransformReadinessDecision(
            capture_batch_id=admitted_input.batch.capture_batch_id,
            slice_name=_SALES_ORDERS_SLICE_NAME,
            is_ready=False,
            reason="missing_sales_orders_payloads",
            matched_payload_count=0,
        )

    if admitted_input.batch.batch_status != "captured":
        return TransformReadinessDecision(
            capture_batch_id=admitted_input.batch.capture_batch_id,
            slice_name=_SALES_ORDERS_SLICE_NAME,
            is_ready=False,
            reason="batch_status_not_captured",
            matched_payload_count=matched_payload_count,
        )

    if admitted_input.batch.transformed_at is not None:
        return TransformReadinessDecision(
            capture_batch_id=admitted_input.batch.capture_batch_id,
            slice_name=_SALES_ORDERS_SLICE_NAME,
            is_ready=False,
            reason="already_transformed",
            matched_payload_count=matched_payload_count,
        )

    return TransformReadinessDecision(
        capture_batch_id=admitted_input.batch.capture_batch_id,
        slice_name=_SALES_ORDERS_SLICE_NAME,
        is_ready=True,
        reason="ready",
        matched_payload_count=matched_payload_count,
    )
