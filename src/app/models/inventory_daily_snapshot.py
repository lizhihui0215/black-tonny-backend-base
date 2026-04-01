from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import ServingBase


class InventoryDailySnapshot(ServingBase):
    __tablename__ = "inventory_daily_snapshot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    analysis_batch_id: Mapped[str] = mapped_column(String(64), index=True)
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    sku_id: Mapped[str] = mapped_column(String(64), index=True)
    on_hand_qty: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    safe_stock_qty: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    capture_batch_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    store_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    style_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    color_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    size_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    season_tag: Mapped[str | None] = mapped_column(String(32), default=None, index=True)
    is_all_season: Mapped[bool | None] = mapped_column(Boolean, default=None)
    is_target_size: Mapped[bool | None] = mapped_column(Boolean, default=None)
    is_active_sale: Mapped[bool | None] = mapped_column(Boolean, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
