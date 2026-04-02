import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Final, Literal

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.crud_analysis_batches import list_analysis_batch_reads
from ..schemas.sales import SalesOrderProjectionFact
from ..schemas.transform import (
    AdmittedTransformInputSnapshot,
    CaptureToSalesOrdersPathReason,
    CaptureToSalesOrdersPathResult,
    TransformReadinessDecision,
)
from .admitted_transform_selector import select_admitted_transform_input
from .capture_batch_lifecycle import mark_capture_batch_failed, mark_capture_batch_transformed
from .sales_orders_projection_contract import apply_sales_orders_projection_contract
from .transform_readiness_evaluator import evaluate_sales_orders_transform_readiness

_SALES_ORDERS_SLICE_NAME: Final[Literal["sales_orders"]] = "sales_orders"
_SALES_ORDERS_SOURCE_ENDPOINT: Final[str] = "/erp/orders"


class _PathFailure(Exception):
    def __init__(self, *, reason: CaptureToSalesOrdersPathReason, error_message: str) -> None:
        super().__init__(error_message)
        self.reason = reason
        self.error_message = error_message


def _parse_required_non_empty_str(value: object, *, field_name: str) -> str:
    if not isinstance(value, str) or value == "":
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _parse_optional_non_empty_str(value: object, *, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or value == "":
        raise ValueError(f"{field_name} must be a non-empty string when provided")
    return value


def _parse_datetime(value: object, *, field_name: str) -> datetime:
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO-8601 string")

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO-8601 string") from exc


def _parse_decimal(value: object, *, field_name: str) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be a decimal-compatible value") from exc


def _build_projection_fact(
    row: object,
    *,
    analysis_batch_id: str,
    capture_batch_id: str,
) -> SalesOrderProjectionFact:
    if not isinstance(row, dict):
        raise ValueError("each `/erp/orders` row must be a JSON object")

    return SalesOrderProjectionFact(
        analysis_batch_id=analysis_batch_id,
        capture_batch_id=capture_batch_id,
        store_id=_parse_optional_non_empty_str(row.get("store_id"), field_name="store_id"),
        order_id=_parse_required_non_empty_str(row.get("order_id"), field_name="order_id"),
        paid_at=_parse_datetime(row.get("paid_at"), field_name="paid_at"),
        paid_amount=_parse_decimal(row.get("paid_amount"), field_name="paid_amount"),
        payment_status=_parse_required_non_empty_str(row.get("payment_status"), field_name="payment_status"),
    )


def _build_sales_orders_projection_facts(
    admitted_input: AdmittedTransformInputSnapshot,
    *,
    analysis_batch_id: str,
) -> list[SalesOrderProjectionFact]:
    facts: list[SalesOrderProjectionFact] = []

    for payload in admitted_input.payloads:
        if payload.source_endpoint != _SALES_ORDERS_SOURCE_ENDPOINT:
            continue

        try:
            parsed_payload = json.loads(payload.payload_json)
        except json.JSONDecodeError as exc:
            raise _PathFailure(
                reason="invalid_sales_orders_payload",
                error_message="invalid `/erp/orders` payload JSON for the first capture-to-serving path",
            ) from exc

        if not isinstance(parsed_payload, dict) or not isinstance(parsed_payload.get("rows"), list):
            raise _PathFailure(
                reason="invalid_sales_orders_payload",
                error_message=(
                    "`/erp/orders` payload JSON must be an object with a `rows` list "
                    "for the first capture-to-serving path"
                ),
            )

        rows = parsed_payload["rows"]
        for row in rows:
            try:
                facts.append(
                    _build_projection_fact(
                        row,
                        analysis_batch_id=analysis_batch_id,
                        capture_batch_id=admitted_input.batch.capture_batch_id,
                    )
                )
            except ValueError as exc:
                raise _PathFailure(
                    reason="invalid_sales_orders_payload",
                    error_message=f"invalid `/erp/orders` row for the first capture-to-serving path: {exc}",
                ) from exc

    if not facts:
        raise _PathFailure(
            reason="invalid_sales_orders_payload",
            error_message=(
                "the first capture-to-serving path found no normalizable `/erp/orders` "
                "rows after readiness passed"
            ),
        )

    return facts


async def _resolve_analysis_batch_id(
    capture_db: AsyncSession,
    *,
    capture_batch_id: str,
) -> str:
    analysis_response = await list_analysis_batch_reads(
        db=capture_db,
        capture_batch_id=capture_batch_id,
        limit=None,
    )
    analysis_rows = analysis_response["data"]

    if not analysis_rows:
        raise _PathFailure(
            reason="missing_analysis_batch",
            error_message=(
                "the first capture-to-serving path requires one linked `analysis_batches` "
                "row before `sales_orders` projection can run"
            ),
        )

    if len(analysis_rows) > 1:
        raise _PathFailure(
            reason="ambiguous_analysis_batch",
            error_message=(
                "the first capture-to-serving path requires exactly one linked "
                "`analysis_batches` row per `capture_batch_id`"
            ),
        )

    return analysis_rows[0].analysis_batch_id


async def _build_failed_result(
    capture_db: AsyncSession,
    *,
    capture_batch_id: str,
    reason: CaptureToSalesOrdersPathReason,
    error_message: str,
    readiness_decision: TransformReadinessDecision,
    analysis_batch_id: str | None = None,
) -> CaptureToSalesOrdersPathResult:
    failed_batch = await mark_capture_batch_failed(
        capture_db,
        capture_batch_id=capture_batch_id,
        error_message=error_message,
    )
    if failed_batch is None:
        raise RuntimeError("capture batch was not readable before the failed lifecycle write")

    return CaptureToSalesOrdersPathResult(
        capture_batch_id=capture_batch_id,
        slice_name=_SALES_ORDERS_SLICE_NAME,
        status="failed",
        reason=reason,
        readiness_decision=readiness_decision,
        analysis_batch_id=analysis_batch_id,
        lifecycle_batch=failed_batch,
        failure_message=error_message,
    )


async def run_capture_to_sales_orders_path(
    capture_db: AsyncSession,
    serving_db: AsyncSession,
    *,
    capture_batch_id: str,
) -> CaptureToSalesOrdersPathResult:
    admitted_input = await select_admitted_transform_input(
        capture_db,
        capture_batch_id=capture_batch_id,
    )
    if admitted_input is None:
        return CaptureToSalesOrdersPathResult(
            capture_batch_id=capture_batch_id,
            slice_name=_SALES_ORDERS_SLICE_NAME,
            status="noop",
            reason="missing_admitted_input",
        )

    readiness_decision = evaluate_sales_orders_transform_readiness(admitted_input)
    if not readiness_decision.is_ready:
        return CaptureToSalesOrdersPathResult(
            capture_batch_id=capture_batch_id,
            slice_name=_SALES_ORDERS_SLICE_NAME,
            status="non_ready",
            reason="not_ready",
            readiness_decision=readiness_decision,
        )

    analysis_batch_id: str | None = None

    try:
        analysis_batch_id = await _resolve_analysis_batch_id(
            capture_db,
            capture_batch_id=capture_batch_id,
        )
        projection_facts = _build_sales_orders_projection_facts(
            admitted_input,
            analysis_batch_id=analysis_batch_id,
        )
    except _PathFailure as exc:
        return await _build_failed_result(
            capture_db,
            capture_batch_id=capture_batch_id,
            reason=exc.reason,
            error_message=exc.error_message,
            readiness_decision=readiness_decision,
            analysis_batch_id=analysis_batch_id,
        )

    try:
        projection_result = await apply_sales_orders_projection_contract(
            serving_db,
            facts=projection_facts,
        )
    except Exception as exc:
        await serving_db.rollback()
        return await _build_failed_result(
            capture_db,
            capture_batch_id=capture_batch_id,
            reason="projection_contract_apply_failed",
            error_message=f"the first capture-to-serving path failed during `sales_orders` contract apply: {exc}",
            readiness_decision=readiness_decision,
            analysis_batch_id=analysis_batch_id,
        )

    transformed_batch = await mark_capture_batch_transformed(
        capture_db,
        capture_batch_id=capture_batch_id,
    )
    if transformed_batch is None:
        raise RuntimeError("capture batch was not readable before the transformed lifecycle write")

    return CaptureToSalesOrdersPathResult(
        capture_batch_id=capture_batch_id,
        slice_name=_SALES_ORDERS_SLICE_NAME,
        status="succeeded",
        reason="applied",
        readiness_decision=readiness_decision,
        analysis_batch_id=analysis_batch_id,
        projection_result=projection_result,
        lifecycle_batch=transformed_batch,
    )
