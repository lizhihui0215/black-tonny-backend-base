from datetime import datetime

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
