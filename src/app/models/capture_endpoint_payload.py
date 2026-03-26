from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import CaptureBase


class CaptureEndpointPayload(CaptureBase):
    __tablename__ = "capture_endpoint_payloads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    capture_batch_id: Mapped[str] = mapped_column(ForeignKey("capture_batches.capture_batch_id"), index=True)
    source_endpoint: Mapped[str] = mapped_column(String(128), index=True)
    payload_json: Mapped[str] = mapped_column(Text)
    checksum: Mapped[str] = mapped_column(String(128), index=True)
    pulled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    route_kind: Mapped[str | None] = mapped_column(String(32), default=None, index=True)
    page_cursor: Mapped[str | None] = mapped_column(String(128), default=None)
    page_no: Mapped[int | None] = mapped_column(Integer, default=None)
    request_params: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
