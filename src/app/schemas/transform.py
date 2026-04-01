from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .capture import CaptureBatchStatus


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
