from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import ServingBase


class SalesOrder(ServingBase):
    __tablename__ = "sales_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    analysis_batch_id: Mapped[str] = mapped_column(String(64), index=True)
    order_id: Mapped[str] = mapped_column(String(64), index=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    paid_amount: Mapped[float] = mapped_column(Float, default=0)
    capture_batch_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    store_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    payment_status: Mapped[str] = mapped_column(String(32), default="paid")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
