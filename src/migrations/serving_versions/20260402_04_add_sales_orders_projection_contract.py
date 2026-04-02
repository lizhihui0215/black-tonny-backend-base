"""Add the first sales_orders serving projection contract.

This migration assumes the existing `sales_orders` table does not already contain
duplicate `(analysis_batch_id, order_id)` pairs.

If historical duplicates exist in a real serving database, a dedicated dedupe
migration must run before this unique constraint can be applied safely.

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
    # The first serving projection contract now formalizes
    # `(analysis_batch_id, order_id)` as the current first-slice identity.
    # This assumes no historical duplicates already exist in `sales_orders`.
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
