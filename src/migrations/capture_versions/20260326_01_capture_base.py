"""Create capture migration baseline.

Revision ID: 20260326_01_capture_base
Revises:
Create Date: 2026-03-26 12:30:00
"""

from collections.abc import Sequence

revision: str = "20260326_01_capture_base"
down_revision: str | None = None
branch_labels: Sequence[str] | None = ("capture",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
