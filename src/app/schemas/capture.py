from datetime import datetime
from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field

from ..constants.capture import (
    CAPTURE_BATCH_DEFAULT_STATUS,
    CAPTURE_BATCH_ID_MAX_LENGTH,
    CAPTURE_CHECKSUM_MAX_LENGTH,
    CAPTURE_PAGE_CURSOR_MAX_LENGTH,
    CAPTURE_ROUTE_KIND_MAX_LENGTH,
    CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH,
    CAPTURE_SOURCE_NAME_MAX_LENGTH,
)

CaptureBatchStatus = Literal["queued", "captured", "partial", "failed", "transformed"]


class CaptureBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str = Field(min_length=1, max_length=CAPTURE_BATCH_ID_MAX_LENGTH)
    batch_status: CaptureBatchStatus = CAPTURE_BATCH_DEFAULT_STATUS
    source_name: str = Field(default="default", min_length=1, max_length=CAPTURE_SOURCE_NAME_MAX_LENGTH)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None
    error_message: str | None = None


class CaptureBatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

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
    source_name: str | None = Field(default=None, min_length=1, max_length=CAPTURE_SOURCE_NAME_MAX_LENGTH)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None
    error_message: str | None = None


class CaptureEndpointPayloadCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str = Field(min_length=1, max_length=CAPTURE_BATCH_ID_MAX_LENGTH)
    source_endpoint: str = Field(min_length=1, max_length=CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH)
    route_kind: str | None = Field(default=None, max_length=CAPTURE_ROUTE_KIND_MAX_LENGTH)
    page_cursor: str | None = Field(default=None, max_length=CAPTURE_PAGE_CURSOR_MAX_LENGTH)
    page_no: int | None = None
    request_params: str | None = None
    payload_json: str = Field(min_length=1)
    checksum: str = Field(min_length=1, max_length=CAPTURE_CHECKSUM_MAX_LENGTH)
    pulled_at: datetime


class CaptureEndpointPayloadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

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

    source_endpoint: str | None = Field(default=None, min_length=1, max_length=CAPTURE_SOURCE_ENDPOINT_MAX_LENGTH)
    route_kind: str | None = Field(default=None, max_length=CAPTURE_ROUTE_KIND_MAX_LENGTH)
    page_cursor: str | None = Field(default=None, max_length=CAPTURE_PAGE_CURSOR_MAX_LENGTH)
    page_no: int | None = None
    request_params: str | None = None
    payload_json: str | None = Field(default=None, min_length=1)
    checksum: str | None = Field(default=None, min_length=1, max_length=CAPTURE_CHECKSUM_MAX_LENGTH)
    pulled_at: datetime | None = None


class CaptureBatchReadListResponse(TypedDict):
    data: list[CaptureBatchRead]
    total_count: int


class CaptureEndpointPayloadReadListResponse(TypedDict):
    data: list[CaptureEndpointPayloadRead]
    total_count: int
