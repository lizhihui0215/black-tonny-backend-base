from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..constants.capture import (
    CAPTURE_BATCH_DEFAULT_STATUS,
    CAPTURE_BATCH_ID_MAX_LENGTH,
    CAPTURE_SOURCE_NAME_MAX_LENGTH,
)
from ..core.db.database import CaptureBase


class CaptureBatch(CaptureBase):
    __tablename__ = "capture_batches"
    __table_args__ = (
        CheckConstraint(
            "batch_status IN ('queued', 'captured', 'partial', 'failed', 'transformed')",
            name="ck_capture_batches_batch_status",
        ),
    )

    capture_batch_id: Mapped[str] = mapped_column(String(CAPTURE_BATCH_ID_MAX_LENGTH), primary_key=True)
    batch_status: Mapped[str] = mapped_column(String(32), default=CAPTURE_BATCH_DEFAULT_STATUS, index=True)
    source_name: Mapped[str] = mapped_column(String(CAPTURE_SOURCE_NAME_MAX_LENGTH), default="default")
    pulled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    transformed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    error_message: Mapped[str | None] = mapped_column(Text, default=None)
