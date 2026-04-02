from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .capture import CaptureBatchRead, CaptureBatchStatus
from .sales import SalesOrderProjectionContractResult


class AdmittedTransformBatchSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str
    batch_status: CaptureBatchStatus
    transformed_at: datetime | None
    error_message: str | None


class AdmittedTransformPayloadSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str
    source_endpoint: str
    payload_json: str
    checksum: str
    pulled_at: datetime


class AdmittedTransformInputSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch: AdmittedTransformBatchSnapshot
    payloads: list[AdmittedTransformPayloadSnapshot]


TransformProjectionSlice = Literal["sales_orders"]
TransformReadinessReason = Literal[
    "ready",
    "missing_sales_orders_payloads",
    "batch_status_not_captured",
    "already_transformed",
]


class TransformReadinessDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str
    slice_name: TransformProjectionSlice
    is_ready: bool
    reason: TransformReadinessReason
    matched_payload_count: int


CaptureToSalesOrdersPathStatus = Literal["noop", "non_ready", "succeeded", "failed"]
CaptureToSalesOrdersPathReason = Literal[
    "missing_admitted_input",
    "not_ready",
    "applied",
    "missing_analysis_batch",
    "ambiguous_analysis_batch",
    "invalid_sales_orders_payload",
    "projection_contract_apply_failed",
]


class CaptureToSalesOrdersPathResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str
    slice_name: TransformProjectionSlice
    status: CaptureToSalesOrdersPathStatus
    reason: CaptureToSalesOrdersPathReason
    readiness_decision: TransformReadinessDecision | None = None
    analysis_batch_id: str | None = None
    projection_result: SalesOrderProjectionContractResult | None = None
    lifecycle_batch: CaptureBatchRead | None = None
    failure_message: str | None = None
