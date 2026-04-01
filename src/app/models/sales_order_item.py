from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import ServingBase


class SalesOrderItem(ServingBase):
    __tablename__ = "sales_order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    analysis_batch_id: Mapped[str] = mapped_column(String(64), index=True)
    order_id: Mapped[str] = mapped_column(String(64), index=True)
    sku_id: Mapped[str] = mapped_column(String(64), index=True)
    capture_batch_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    style_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    color_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    size_code: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
