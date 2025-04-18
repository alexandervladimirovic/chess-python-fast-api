"""update timestamp fields.

Revision ID: 72fb27e548e5
Revises: c1cb93654ec0
Create Date: 2025-04-01 20:34:51.943776

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "72fb27e548e5"
down_revision: Union[str, None] = "c1cb93654ec0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "countries",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "countries",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "privileges",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "privileges",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "profiles",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "profiles",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "ranks",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "ranks",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "roles",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "roles",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "roles",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "roles",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "ranks",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "ranks",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "profiles",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        "profiles",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "privileges",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "privileges",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "countries",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "countries",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###
