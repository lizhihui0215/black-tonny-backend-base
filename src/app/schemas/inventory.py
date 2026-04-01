from datetime import date, datetime
from decimal import Decimal
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field


class InventoryCurrentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_batch_id: str = Field(min_length=1, max_length=64)
    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    sku_id: str = Field(min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    on_hand_qty: Decimal = Field(max_digits=18, decimal_places=2)
    safe_stock_qty: Decimal = Field(max_digits=18, decimal_places=2)
    season_tag: str | None = Field(default=None, min_length=1, max_length=32)
    is_all_season: bool | None = None
    is_target_size: bool | None = None
    is_active_sale: bool | None = None


class InventoryCurrentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    analysis_batch_id: str
    capture_batch_id: str | None
    store_id: str | None
    sku_id: str
    style_code: str | None
    color_code: str | None
    size_code: str | None
    on_hand_qty: Decimal
    safe_stock_qty: Decimal
    season_tag: str | None
    is_all_season: bool | None
    is_target_size: bool | None
    is_active_sale: bool | None
    updated_at: datetime


class InventoryCurrentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    on_hand_qty: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    safe_stock_qty: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    season_tag: str | None = Field(default=None, min_length=1, max_length=32)
    is_all_season: bool | None = None
    is_target_size: bool | None = None
    is_active_sale: bool | None = None


class InventoryCurrentReadListResponse(TypedDict):
    data: list[InventoryCurrentRead]
    total_count: int


class InventoryDailySnapshotCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis_batch_id: str = Field(min_length=1, max_length=64)
    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    snapshot_date: date
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    sku_id: str = Field(min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    on_hand_qty: Decimal = Field(max_digits=18, decimal_places=2)
    safe_stock_qty: Decimal = Field(max_digits=18, decimal_places=2)
    season_tag: str | None = Field(default=None, min_length=1, max_length=32)
    is_all_season: bool | None = None
    is_target_size: bool | None = None
    is_active_sale: bool | None = None


class InventoryDailySnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    analysis_batch_id: str
    capture_batch_id: str | None
    snapshot_date: date
    store_id: str | None
    sku_id: str
    style_code: str | None
    color_code: str | None
    size_code: str | None
    on_hand_qty: Decimal
    safe_stock_qty: Decimal
    season_tag: str | None
    is_all_season: bool | None
    is_target_size: bool | None
    is_active_sale: bool | None
    created_at: datetime


class InventoryDailySnapshotUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture_batch_id: str | None = Field(default=None, min_length=1, max_length=64)
    snapshot_date: date | None = None
    store_id: str | None = Field(default=None, min_length=1, max_length=64)
    style_code: str | None = Field(default=None, min_length=1, max_length=64)
    color_code: str | None = Field(default=None, min_length=1, max_length=64)
    size_code: str | None = Field(default=None, min_length=1, max_length=64)
    on_hand_qty: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    safe_stock_qty: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    season_tag: str | None = Field(default=None, min_length=1, max_length=32)
    is_all_season: bool | None = None
    is_target_size: bool | None = None
    is_active_sale: bool | None = None


class InventoryDailySnapshotReadListResponse(TypedDict):
    data: list[InventoryDailySnapshotRead]
    total_count: int
