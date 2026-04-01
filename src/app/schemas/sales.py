from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field


class SalesOrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_batch_id: str = Field(min_length=1, max_length=64)
    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    order_id: str = Field(min_length=1, max_length=64)
    paid_at: datetime
    paid_amount: float = 0
    payment_status: str = Field(default="paid", min_length=1, max_length=32)


class SalesOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    analysis_batch_id: str
    capture_batch_id: str | None
    store_id: str | None
    order_id: str
    paid_at: datetime
    paid_amount: float
    payment_status: str
    created_at: datetime
    updated_at: datetime


class SalesOrderUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    paid_at: datetime | None = None
    paid_amount: float | None = None
    payment_status: str | None = Field(default=None, min_length=1, max_length=32)


class SalesOrderReadListResponse(TypedDict):
    data: list[SalesOrderRead]
    total_count: int


class SalesOrderItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_batch_id: str = Field(min_length=1, max_length=64)
    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    order_id: str = Field(min_length=1, max_length=64)
    sku_id: str = Field(min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    quantity: float = 0


class SalesOrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    analysis_batch_id: str
    capture_batch_id: str | None
    order_id: str
    sku_id: str
    style_code: str | None
    color_code: str | None
    size_code: str | None
    quantity: float
    created_at: datetime
    updated_at: datetime


class SalesOrderItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    quantity: float | None = None


class SalesOrderItemReadListResponse(TypedDict):
    data: list[SalesOrderItemRead]
    total_count: int
