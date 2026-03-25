"""Create user and token_blacklist tables.

Revision ID: 20260325_01
Revises:
Create Date: 2026-03-25 22:20:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260325_01"
down_revision: str | None = None
branch_labels: Sequence[str] | None = ("serving",)
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tier",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("profile_image_url", sa.String(), nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tier_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tier_id"], ["tier.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_is_deleted"), "user", ["is_deleted"], unique=False)
    op.create_index(op.f("ix_user_tier_id"), "user", ["tier_id"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "rate_limit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tier_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("limit", sa.Integer(), nullable=False),
        sa.Column("period", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tier_id"], ["tier.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_rate_limit_tier_id"), "rate_limit", ["tier_id"], unique=False)
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_token_blacklist_token"), "token_blacklist", ["token"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_token_blacklist_token"), table_name="token_blacklist")
    op.drop_table("token_blacklist")
    op.drop_index(op.f("ix_rate_limit_tier_id"), table_name="rate_limit")
    op.drop_table("rate_limit")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_tier_id"), table_name="user")
    op.drop_index(op.f("ix_user_is_deleted"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("tier")
