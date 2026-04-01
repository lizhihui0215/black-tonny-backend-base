"""Add serving inventory projection persistence tables.

Revision ID: 20260401_03
Revises: 20260401_02
Create Date: 2026-04-01 23:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260401_03"
down_revision: str | None = "20260401_02"
branch_labels: Sequence[str] | None = ("serving",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "inventory_current",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_batch_id", sa.String(length=64), nullable=False),
        sa.Column("sku_id", sa.String(length=64), nullable=False),
        sa.Column("on_hand_qty", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("safe_stock_qty", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=True),
        sa.Column("store_id", sa.String(length=64), nullable=True),
        sa.Column("style_code", sa.String(length=64), nullable=True),
        sa.Column("color_code", sa.String(length=64), nullable=True),
        sa.Column("size_code", sa.String(length=64), nullable=True),
        sa.Column("season_tag", sa.String(length=32), nullable=True),
        sa.Column("is_all_season", sa.Boolean(), nullable=True),
        sa.Column("is_target_size", sa.Boolean(), nullable=True),
        sa.Column("is_active_sale", sa.Boolean(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_inventory_current_analysis_batch_id"),
        "inventory_current",
        ["analysis_batch_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_current_capture_batch_id"),
        "inventory_current",
        ["capture_batch_id"],
        unique=False,
    )
    op.create_index(op.f("ix_inventory_current_color_code"), "inventory_current", ["color_code"], unique=False)
    op.create_index(op.f("ix_inventory_current_season_tag"), "inventory_current", ["season_tag"], unique=False)
    op.create_index(op.f("ix_inventory_current_size_code"), "inventory_current", ["size_code"], unique=False)
    op.create_index(op.f("ix_inventory_current_sku_id"), "inventory_current", ["sku_id"], unique=False)
    op.create_index(op.f("ix_inventory_current_store_id"), "inventory_current", ["store_id"], unique=False)
    op.create_index(op.f("ix_inventory_current_style_code"), "inventory_current", ["style_code"], unique=False)

    op.create_table(
        "inventory_daily_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_batch_id", sa.String(length=64), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("sku_id", sa.String(length=64), nullable=False),
        sa.Column("on_hand_qty", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("safe_stock_qty", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=True),
        sa.Column("store_id", sa.String(length=64), nullable=True),
        sa.Column("style_code", sa.String(length=64), nullable=True),
        sa.Column("color_code", sa.String(length=64), nullable=True),
        sa.Column("size_code", sa.String(length=64), nullable=True),
        sa.Column("season_tag", sa.String(length=32), nullable=True),
        sa.Column("is_all_season", sa.Boolean(), nullable=True),
        sa.Column("is_target_size", sa.Boolean(), nullable=True),
        sa.Column("is_active_sale", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_analysis_batch_id"),
        "inventory_daily_snapshot",
        ["analysis_batch_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_capture_batch_id"),
        "inventory_daily_snapshot",
        ["capture_batch_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_color_code"),
        "inventory_daily_snapshot",
        ["color_code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_season_tag"),
        "inventory_daily_snapshot",
        ["season_tag"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_size_code"),
        "inventory_daily_snapshot",
        ["size_code"],
        unique=False,
    )
    op.create_index(op.f("ix_inventory_daily_snapshot_sku_id"), "inventory_daily_snapshot", ["sku_id"], unique=False)
    op.create_index(
        op.f("ix_inventory_daily_snapshot_snapshot_date"),
        "inventory_daily_snapshot",
        ["snapshot_date"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_store_id"),
        "inventory_daily_snapshot",
        ["store_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_inventory_daily_snapshot_style_code"),
        "inventory_daily_snapshot",
        ["style_code"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_inventory_daily_snapshot_style_code"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_store_id"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_snapshot_date"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_sku_id"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_size_code"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_season_tag"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_color_code"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_capture_batch_id"), table_name="inventory_daily_snapshot")
    op.drop_index(op.f("ix_inventory_daily_snapshot_analysis_batch_id"), table_name="inventory_daily_snapshot")
    op.drop_table("inventory_daily_snapshot")

    op.drop_index(op.f("ix_inventory_current_style_code"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_store_id"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_sku_id"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_size_code"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_season_tag"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_color_code"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_capture_batch_id"), table_name="inventory_current")
    op.drop_index(op.f("ix_inventory_current_analysis_batch_id"), table_name="inventory_current")
    op.drop_table("inventory_current")
