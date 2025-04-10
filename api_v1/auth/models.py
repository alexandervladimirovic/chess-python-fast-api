from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from mixins import DescriptionMixin, TimestampMixin
from utils import now_with_tz_utc

from .enums import GenderEnum

# Max length for 'User' model
MAX_LENGTH_USERNAME = 30
MAX_LENGTH_EMAIL = 255
MAX_LENGTH_PASSWORD_HASH = 255
# Max length for 'Profile' model
MAX_LENGTH_NAME = 30
MAX_LENGTH_SURNAME = 40
MAX_LENGTH_BIOGRAPHY = 300
MAX_LENGTH_AVATAR_URL = 255
# Max length for 'Country' model
MAX_LENGTH_COUNTRY_NAME = 50
MAX_LENGTH_COUNTRY_CODE = 2
# Max length for 'Rank' model
MAX_LENGTH_RANK_NAME = 30
MAX_LENGTH_RANK_ABBREVIATION = 3
# Max length for 'Role' model
MAX_LENGTH_ROLE_NAME = 50
# Max length for 'Privilege' model
MAX_LENGTH_PRIVILEGE_NAME = 100


class User(Base):
    """Represents user in system with basic account information.

    Attributes:
        uuid (UUID): Unique identifier for the user (UUID v4).
        username (str): Unique username for user.
        email (str): Unique e-mail for user.
        password_hash (str): Hashed password of user for authentication.
        date_joined (datetime): Date and time when the user registered (UTC).
        last_login (datetime): Last date and time when the user logged in (UTC).
        is_active (bool): Flag whether user account is active. Default is True.

    Relationships:
        profile (Profile): One-to-one relationship with the user profile.

    """

    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(unique=True, default=uuid4)
    username: Mapped[str] = mapped_column(
        String(MAX_LENGTH_USERNAME),
        index=True,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(MAX_LENGTH_EMAIL),
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(MAX_LENGTH_PASSWORD_HASH))
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz_utc,
        server_default=func.now(),
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz_utc,
        onupdate=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    profile: Mapped[Profile] = relationship(back_populates="user")
    roles: Mapped[list[Role]] = relationship(
        secondary="users_roles_association_table",
        back_populates="users",
    )

    def __repr__(self):
        return f"<User({self.id=}, {self.username=}, {self.email=})>"


class Profile(TimestampMixin, Base):
    """Contains detailed personal information for user.

    Attributes:
        name (str): First name for user (Optional).
        surname (str): Last name for user (Optional).
        gender (GenderEnum): Gender of user. It uses `GenderEnum` for possible values.
        date_of_birth: Birth date of the user (Optional).
        biography (str): Short biography for user (Optional).
        avatar_url (str): URL avatar for user (Optional).
        created_at (datetime): Timestamp created role. Submitted from: TimestampMixin.
        updated_at (datetime): Timestamp updsted role. Submitted from: TimestampMixin.
        user_id (int): ID of user associated with profile (One-To-One).
        country_id (int): ID of user country, linked to `Country` model.
        rank_id (int): ID of user rank, linked to `Rank` model. Default is None.

    Relationships:
        user (User): One-To-One relationship with `User` model.
        country (Country): One-To-Many relationship with the `Country` model.
        rank (Rank): One-To-Many relationship with the `Rank` model.

    """

    __tablename__ = "profiles"

    name: Mapped[Optional[str]] = mapped_column(String(MAX_LENGTH_NAME))
    surname: Mapped[Optional[str]] = mapped_column(String(MAX_LENGTH_SURNAME))
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="gender_enum"),
        default=GenderEnum.NOT_DEFINED,
    )
    date_of_birth: Mapped[Optional[date]] = mapped_column()
    biography: Mapped[Optional[str]] = mapped_column(String(MAX_LENGTH_BIOGRAPHY))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(MAX_LENGTH_AVATAR_URL))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    rank_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ranks.id"),
        default=None,
    )

    user: Mapped[User] = relationship(back_populates="profile")
    country: Mapped[Country] = relationship(back_populates="profiles")
    rank: Mapped[Optional[Rank]] = relationship(back_populates="profiles")

    def __repr__(self):
        return f"<Profile({self.user_id=}, {self.name if self.name else 'No name'})>"


class Country(DescriptionMixin, TimestampMixin, Base):
    """Represents a country where user is located or associated with.

    Attributes:
        name (str): The name of the country. This is unique.
        code (str): The ISO 2-letter code of the country. This is unique.
        description(str): Optional description for country. Submitted from:
        DescriptionMixin.
        created_at (datetime): Timestamp created country. Submitted from:
        TimestampMixin.
        updated_at (datetime): Timestamp updated country. Submitted from:
        TimestampMixin.

    Relationships:
        profiles (Profile): Many-To-One relationship with the `Profile` model,
        representing all users from this country.

    """

    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_COUNTRY_NAME),
        unique=True,
    )
    code: Mapped[str] = mapped_column(
        String(MAX_LENGTH_COUNTRY_CODE),
        unique=True,
    )

    profiles: Mapped[Profile] = relationship(back_populates="country")

    def __repr__(self):
        return f"<Country({self.name} ({self.code}))>"


class Rank(DescriptionMixin, TimestampMixin, Base):
    """Represents rank associated with user profile.

    Attributes:
        name (str): The name of rank (e.g., Grandmaster, International Master).
        abbreviation (str): The abbreviation for rank (e.g., GM, IM).
        description(str): Optional description for rank. Submitted from:
        DescriptionMixin.
        created_at (datetime): Timestamp created rank. Submitted from: TimestampMixin.
        updated_at (datetime): Timestamp updated rank. Submitted from: TimestampMixin.

    Relationships:
        profiles (Profile): Many-To-One relationship with `Profile` model,
        representing all users with this rank.

    """

    __tablename__ = "ranks"

    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_RANK_NAME),
        unique=True,
    )
    abbreviation: Mapped[str] = mapped_column(
        String(MAX_LENGTH_RANK_ABBREVIATION),
        unique=True,
    )

    profiles: Mapped[Profile] = relationship(back_populates="rank")

    def __repr__(self):
        return f"<Rank({self.name} ({self.abbreviation}))>"


class Role(DescriptionMixin, TimestampMixin, Base):
    """Represents a user role in database.

    Model is used to define various roles that users can have, such as
    'player', 'admin', 'moderator', etc.

    Attributes:
        name (str): Unique name of role, e.g., 'player', 'admin'.
        description(str): Optional description for roles. Submitted from:
        DescriptionMixin.
        created_at (datetime): Timestamp created role. Submitted from: TimestampMixin.
        updated_at (datetime): Timestamp updated role. Submitted from: TimestampMixin.

    """

    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_ROLE_NAME),
        unique=True,
    )

    users: Mapped[list[User]] = relationship(
        secondary="users_roles_association_table",
        back_populates="roles",
    )
    privileges: Mapped[list[Privilege]] = relationship(
        secondary="roles_privileges_association_table",
        back_populates="roles",
    )

    def __repr__(self):
        return f"<Role({self.name})>"


class Privilege(DescriptionMixin, TimestampMixin, Base):
    """Privileges can define various permissions or capabilities that role possesses.

    Attributes:
        name (str): Unique name of privilege, e.g., 'create', 'delete'.
        description(str): Optional description for privilege. Submitted from:
        DescriptionMixin.
        created_at (datetime): Timestamp created privilege. Submitted from:
        TimestampMixin.
        updated_at (datetime): Timestamp updated privilege. Submitted from:
        TimestampMixin.

    """

    __tablename__ = "privileges"

    name: Mapped[str] = mapped_column(String(MAX_LENGTH_PRIVILEGE_NAME))

    roles: Mapped[list[Role]] = relationship(
        secondary="roles_privileges_association_table",
        back_populates="privileges",
    )

    def __repr__(self):
        return f"<Privilege({self.name})>"
