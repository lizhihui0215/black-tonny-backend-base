"""Add analysis batches table.

Revision ID: 20260401_01_add_analysis_batches_table
Revises: 20260326_03_add_capture_batch_status_check
Create Date: 2026-04-01 12:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260401_01_add_analysis_batches_table"
down_revision: str | None = "20260326_03_add_capture_batch_status_check"
branch_labels: Sequence[str] | None = ("capture",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "analysis_batches",
        sa.Column("analysis_batch_id", sa.String(length=64), nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=True),
        sa.Column("batch_status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("source_endpoint", sa.String(length=128), nullable=True),
        sa.Column("pulled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("transformed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("analysis_batch_id"),
    )
    op.create_index(
        op.f("ix_analysis_batches_capture_batch_id"),
        "analysis_batches",
        ["capture_batch_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_analysis_batches_capture_batch_id"), table_name="analysis_batches")
    op.drop_table("analysis_batches")
