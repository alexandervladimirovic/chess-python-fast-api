from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class User(Base):
    """Model for users.

    Attributes:
        username (str): Unique username for user.
        email (str): Unique e-mail for user.
        password_hash (str): Hashed password user.
        date_joined (datetime): Datetime of user registration.
        last_login (datetime): Datetime of user last login.
        is_active (bool): Activity status user.

    Link:
        profile (Profile): Link to user profile (One-To-One).

    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    date_joined: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    last_login: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # link to 'Profile' model
    profile: Mapped["Profile"] = relationship(back_populates="user")


class Profile(Base):
    """Model profile user. Contains the user personal info.

    Attributes:
        name (str): First name for user (Optional).
        surname (str): Last name for user (Optional).
        date_of_birth: Date of birth for user (Optional).
        biography (str): Short biography for user (Optional).
        avatar_url (str): URL avatar for user (Optional).
        updated_at (datetime): Datetime last update profile.
        user_id (int): ID of user associated with profile (One-To-One).

    Link:
        user (User): Link to user profile (One-To-One).

    """

    __tablename__ = "profiles"

    name: Mapped[Optional[str]] = mapped_column(String(25))
    surname: Mapped[Optional[str]] = mapped_column(String(35))
    date_of_birth: Mapped[Optional[date]] = mapped_column()
    biography: Mapped[Optional[str]] = mapped_column(String(300))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), unique=True)

    # link to 'User' model
    user: Mapped["User"] = relationship(back_populates="profile")
