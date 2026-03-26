"""Add capture batch status check constraint.

Revision ID: 20260326_03_add_capture_batch_status_check
Revises: 20260326_02_add_capture_contract_tables
Create Date: 2026-03-26 22:10:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260326_03_add_capture_batch_status_check"
down_revision: str | None = "20260326_02_add_capture_contract_tables"
branch_labels: Sequence[str] | None = ("capture",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_capture_batches_batch_status",
        "capture_batches",
        sa.text("batch_status IN ('queued', 'captured', 'partial', 'failed', 'transformed')"),
    )


def downgrade() -> None:
    op.drop_constraint("ck_capture_batches_batch_status", "capture_batches", type_="check")
