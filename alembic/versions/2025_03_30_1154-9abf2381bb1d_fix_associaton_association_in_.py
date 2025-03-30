"""fix associaton > association in association roles-privilege table.

Revision ID: 9abf2381bb1d
Revises: c59700bf726c
Create Date: 2025-03-30 11:54:05.028262

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9abf2381bb1d"
down_revision: Union[str, None] = "c59700bf726c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("roles_privileges_associaton_table")
    op.create_table(
        "roles_privileges_association_table",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("privilege_id", sa.Integer(), nullable=False),
        sa.Column(
            "assigned_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["privilege_id"],
            ["privileges.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "role_id", "privilege_id", name="idx_unique_role_privilege"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("roles_privileges_association_table")
    op.create_table(
        "roles_privileges_associaton_table",
        sa.Column("role_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("privilege_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "assigned_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["privilege_id"],
            ["privileges.id"],
            name="roles_privileges_associaton_table_privilege_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name="roles_privileges_associaton_table_role_id_fkey",
        ),
        sa.UniqueConstraint(
            "role_id", "privilege_id", name="idx_unique_role_privilege"
        ),
    )
    # ### end Alembic commands ###
