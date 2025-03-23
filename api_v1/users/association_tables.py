from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Table,
    UniqueConstraint,
    func,
)

from core.models.base import Base

users_roles_association_table = Table(
    "users_roles_association_table",
    Base.metadata,
    Column("users_roles_id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("role_id", ForeignKey("roles.id"), nullable=False),
    Column("assigned_at", DateTime, default=datetime.now, server_default=func.now()),
    UniqueConstraint("user_id", "role_id", name="idx_unique_user_role"),
)
