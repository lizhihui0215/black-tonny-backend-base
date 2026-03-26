"""Add minimal capture contract tables.

Revision ID: 20260326_02_add_capture_contract_tables
Revises: 20260326_01_capture_base
Create Date: 2026-03-26 21:20:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260326_02_add_capture_contract_tables"
down_revision: str | None = "20260326_01_capture_base"
branch_labels: Sequence[str] | None = ("capture",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "capture_batches",
        sa.Column("capture_batch_id", sa.String(length=64), nullable=False),
        sa.Column("batch_status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("source_name", sa.String(length=128), nullable=False, server_default="default"),
        sa.Column("pulled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("transformed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("capture_batch_id"),
    )
    op.create_index(op.f("ix_capture_batches_batch_status"), "capture_batches", ["batch_status"], unique=False)
    op.create_table(
        "capture_endpoint_payloads",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=False),
        sa.Column("source_endpoint", sa.String(length=128), nullable=False),
        sa.Column("route_kind", sa.String(length=32), nullable=True),
        sa.Column("page_cursor", sa.String(length=128), nullable=True),
        sa.Column("page_no", sa.Integer(), nullable=True),
        sa.Column("request_params", sa.Text(), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=False),
        sa.Column("pulled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_capture_endpoint_payloads_capture_batch_id"),
        "capture_endpoint_payloads",
        ["capture_batch_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_capture_endpoint_payloads_checksum"),
        "capture_endpoint_payloads",
        ["checksum"],
        unique=False,
    )
    op.create_index(
        op.f("ix_capture_endpoint_payloads_route_kind"),
        "capture_endpoint_payloads",
        ["route_kind"],
        unique=False,
    )
    op.create_index(
        op.f("ix_capture_endpoint_payloads_source_endpoint"),
        "capture_endpoint_payloads",
        ["source_endpoint"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_capture_endpoint_payloads_source_endpoint"), table_name="capture_endpoint_payloads")
    op.drop_index(op.f("ix_capture_endpoint_payloads_route_kind"), table_name="capture_endpoint_payloads")
    op.drop_index(op.f("ix_capture_endpoint_payloads_checksum"), table_name="capture_endpoint_payloads")
    op.drop_index(op.f("ix_capture_endpoint_payloads_capture_batch_id"), table_name="capture_endpoint_payloads")
    op.drop_table("capture_endpoint_payloads")
    op.drop_index(op.f("ix_capture_batches_batch_status"), table_name="capture_batches")
    op.drop_table("capture_batches")
