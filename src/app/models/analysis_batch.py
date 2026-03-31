from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import CaptureBase


class AnalysisBatch(CaptureBase):
    __tablename__ = "analysis_batches"

    analysis_batch_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    capture_batch_id: Mapped[str | None] = mapped_column(String(64), default=None, index=True)
    batch_status: Mapped[str] = mapped_column(String(32), default="queued")
    source_endpoint: Mapped[str | None] = mapped_column(String(128), default=None)
    pulled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    transformed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
