"""Add serving sales projection persistence tables.

Revision ID: 20260401_02
Revises: 20260325_01
Create Date: 2026-04-01 11:10:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260401_02"
down_revision: str | None = "20260325_01"
branch_labels: Sequence[str] | None = ("serving",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sales_orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_batch_id", sa.String(length=64), nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=True),
        sa.Column("store_id", sa.String(length=64), nullable=True),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("paid_amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("payment_status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_orders_analysis_batch_id"), "sales_orders", ["analysis_batch_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_capture_batch_id"), "sales_orders", ["capture_batch_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_order_id"), "sales_orders", ["order_id"], unique=False)
    op.create_index(op.f("ix_sales_orders_paid_at"), "sales_orders", ["paid_at"], unique=False)
    op.create_index(op.f("ix_sales_orders_store_id"), "sales_orders", ["store_id"], unique=False)

    op.create_table(
        "sales_order_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("analysis_batch_id", sa.String(length=64), nullable=False),
        sa.Column("capture_batch_id", sa.String(length=64), nullable=True),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("sku_id", sa.String(length=64), nullable=False),
        sa.Column("style_code", sa.String(length=64), nullable=True),
        sa.Column("color_code", sa.String(length=64), nullable=True),
        sa.Column("size_code", sa.String(length=64), nullable=True),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sales_order_items_analysis_batch_id"),
        "sales_order_items",
        ["analysis_batch_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_sales_order_items_capture_batch_id"),
        "sales_order_items",
        ["capture_batch_id"],
        unique=False,
    )
    op.create_index(op.f("ix_sales_order_items_color_code"), "sales_order_items", ["color_code"], unique=False)
    op.create_index(op.f("ix_sales_order_items_order_id"), "sales_order_items", ["order_id"], unique=False)
    op.create_index(op.f("ix_sales_order_items_size_code"), "sales_order_items", ["size_code"], unique=False)
    op.create_index(op.f("ix_sales_order_items_sku_id"), "sales_order_items", ["sku_id"], unique=False)
    op.create_index(op.f("ix_sales_order_items_style_code"), "sales_order_items", ["style_code"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_sales_order_items_style_code"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_sku_id"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_size_code"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_order_id"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_color_code"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_capture_batch_id"), table_name="sales_order_items")
    op.drop_index(op.f("ix_sales_order_items_analysis_batch_id"), table_name="sales_order_items")
    op.drop_table("sales_order_items")

    op.drop_index(op.f("ix_sales_orders_store_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_paid_at"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_order_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_capture_batch_id"), table_name="sales_orders")
    op.drop_index(op.f("ix_sales_orders_analysis_batch_id"), table_name="sales_orders")
    op.drop_table("sales_orders")
