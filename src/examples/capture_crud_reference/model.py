from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.db.database import Base


class ExampleRecord(Base):
    """Reference-only SQLAlchemy model for future capture-side CRUD modules."""

    __tablename__ = "example_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    external_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
