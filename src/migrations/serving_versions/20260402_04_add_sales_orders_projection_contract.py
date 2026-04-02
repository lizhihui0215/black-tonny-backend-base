"""Add the first sales_orders serving projection contract.

Revision ID: 20260402_04
Revises: 20260401_03
Create Date: 2026-04-02 10:20:00
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260402_04"
down_revision: str | None = "20260401_03"
branch_labels: Sequence[str] | None = ("serving",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_sales_orders_analysis_batch_id_order_id",
        "sales_orders",
        ["analysis_batch_id", "order_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_sales_orders_analysis_batch_id_order_id",
        "sales_orders",
        type_="unique",
    )
