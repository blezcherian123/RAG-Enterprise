"""Create tenant and user tables with database enforced roles.

Revision ID: 0001_initial
Revises:
"""
import uuid

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "tenants" not in tables:
        op.create_table(
            "tenants",
            sa.Column("id", sa.String(), primary_key=True, nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False, unique=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )
        op.create_index("ix_tenants_name", "tenants", ["name"], unique=True)

    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("tenant_id", sa.String(), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=True),
            sa.Column("hashed_password", sa.String(length=255), nullable=False),
            sa.Column("role", sa.String(length=32), server_default="employee", nullable=False),
            sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
            sa.CheckConstraint("role IN ('admin', 'hr', 'employee', 'finance', 'c_level')", name="ck_users_valid_role"),
        )
        op.create_index("ix_users_tenant_id", "users", ["tenant_id"])
        op.create_index("ix_users_email", "users", ["email"])
    else:
        user_columns = {column["name"] for column in sa.inspect(bind).get_columns("users")}
        if "role" not in user_columns:
            op.add_column("users", sa.Column("role", sa.String(length=32), server_default="employee", nullable=False))
        constraints = {constraint["name"] for constraint in sa.inspect(bind).get_check_constraints("users")}
        if "ck_users_valid_role" not in constraints:
            op.create_check_constraint(
                "ck_users_valid_role",
                "users",
                "role IN ('admin', 'hr', 'employee', 'finance', 'c_level')",
            )

    tenant_exists = bind.execute(sa.text("SELECT 1 FROM tenants WHERE name = :name"), {"name": "default"}).first()
    if not tenant_exists:
        bind.execute(
            sa.text("INSERT INTO tenants (id, name) VALUES (:id, :name)"),
            {"id": str(uuid.uuid4()), "name": "default"},
        )


def downgrade() -> None:
    # This migration also adopts legacy databases. Keep data intact; make changes
    # through a later forward migration instead of destructively reversing it.
    pass
