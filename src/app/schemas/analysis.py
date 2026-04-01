from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field


class AnalysisBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_batch_id: str = Field(min_length=1, max_length=64)
    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    batch_status: str = Field(default="queued", min_length=1, max_length=32)
    source_endpoint: str | None = Field(default=None, min_length=1, max_length=128)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None


class AnalysisBatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    analysis_batch_id: str
    capture_batch_id: str | None
    batch_status: str
    source_endpoint: str | None
    pulled_at: datetime | None
    transformed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class AnalysisBatchUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    batch_status: str | None = Field(default=None, min_length=1, max_length=32)
    source_endpoint: str | None = Field(default=None, min_length=1, max_length=128)
    pulled_at: datetime | None = None
    transformed_at: datetime | None = None


class AnalysisBatchReadListResponse(TypedDict):
    data: list[AnalysisBatchRead]
    total_count: int
