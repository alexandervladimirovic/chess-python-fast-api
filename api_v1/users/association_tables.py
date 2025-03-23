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

roles_privileges_association_table = Table(
    "roles_privileges_associaton_table",
    Base.metadata,
    Column("roles_privileges_id", Integer, primary_key=True),
    Column("role_id", ForeignKey("roles.id"), nullable=False),
    Column("privilege_id", ForeignKey("privileges.id"), nullable=False),
    Column("assigned_at", DateTime, default=datetime.now, server_default=func.now()),
    UniqueConstraint("role_id", "privilege_id", name="idx_unique_role_privilege"),
)
