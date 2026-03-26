from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CaptureBatchStatus = Literal["queued", "captured", "partial", "failed", "transformed"]


class CaptureBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str = Field(min_length=1, max_length=64)
    batch_status: CaptureBatchStatus = "queued"
    source_name: str = Field(default="default", min_length=1, max_length=128)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None
    error_message: str | None = None


class CaptureBatchRead(BaseModel):
    capture_batch_id: str
    batch_status: CaptureBatchStatus
    source_name: str
    pulled_at: datetime | None
    transformed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    error_message: str | None


class CaptureBatchUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    batch_status: CaptureBatchStatus | None = None
    source_name: str | None = Field(default=None, min_length=1, max_length=128)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None
    updated_at: datetime | None = None
    error_message: str | None = None


class CaptureEndpointPayloadCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str = Field(min_length=1, max_length=64)
    source_endpoint: str = Field(min_length=1, max_length=128)
    route_kind: str | None = Field(default=None, max_length=32)
    page_cursor: str | None = Field(default=None, max_length=128)
    page_no: int | None = None
    request_params: str | None = None
    payload_json: str = Field(min_length=1)
    checksum: str = Field(min_length=1, max_length=128)
    pulled_at: datetime


class CaptureEndpointPayloadRead(BaseModel):
    id: int
    capture_batch_id: str
    source_endpoint: str
    route_kind: str | None
    page_cursor: str | None
    page_no: int | None
    request_params: str | None
    payload_json: str
    checksum: str
    pulled_at: datetime
    created_at: datetime


class CaptureEndpointPayloadUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_endpoint: str | None = Field(default=None, min_length=1, max_length=128)
    route_kind: str | None = Field(default=None, max_length=32)
    page_cursor: str | None = Field(default=None, max_length=128)
    page_no: int | None = None
    request_params: str | None = None
    payload_json: str | None = Field(default=None, min_length=1)
    checksum: str | None = Field(default=None, min_length=1, max_length=128)
    pulled_at: datetime | None = None
