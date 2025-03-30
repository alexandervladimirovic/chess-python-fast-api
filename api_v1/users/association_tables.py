from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class UserRoleAssociation(Base):
    """Represents association between users and roles in system.

    Model is used to associate a user with a specific role. It also stores
    timestamp when the role was assigned to user.

    Attributes:
        user_id (int): ID of user.
        role_id (int): ID of role.
        assigned_at (datetime): Timestamp when the role was assigned to user.

    Constraints:
        Unique Constraint: Ensures that user can only have one unique role at time.

    """

    __tablename__ = "users_roles_association_table"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="idx_unique_user_role"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    assigned_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )


class RolePrivilegeAssociation(Base):
    """Represents association between roles and privileges in system.

    This model is used to associate role with specific privilege. It also stores
    the timestamp when privilege was assigned to role.

    Attributes:
        role_id (int): ID of role.
        privilege_id (int): ID of privilege.
        assigned_at (datetime): Timestamp when the privilege was assigned to role.

    Constraints:
        UniqueConstraint: Ensures that role can only have one unique privilege at
        time.

    """

    __tablename__ = "roles_privileges_association_table"
    __table_args__ = (
        UniqueConstraint("role_id", "privilege_id", name="idx_unique_role_privilege"),
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    privilege_id: Mapped[int] = mapped_column(ForeignKey("privileges.id"))
    assigned_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )
