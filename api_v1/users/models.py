from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


class User(Base):
    """Model for users.

    Represents user in system with basic account information.

    Attributes:
        username (str): Unique username for user.
        email (str): Unique e-mail for user.
        password_hash (str): Hashed password of user for authentication.
        date_joined (datetime): Date and time when the user registered.
        last_login (datetime): Last date and time when the user logged in.
        is_active (bool): Flag whether user account is active. Default is True.

    Relationships:
        profile (Profile): One-to-one relationship with the user profile.

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

    def __repr__(self):
        return f"<User({self.id=}, {self.username=}, {self.email=})>"


class Profile(Base):
    """Model profile user.

    Contains detailed personal information for user.

    Attributes:
        name (str): First name for user (Optional).
        surname (str): Last name for user (Optional).
        gender (GenderEnum): Gender of user. It uses `GenderEnum` for possible values.
        date_of_birth: Birth date of the user (Optional).
        biography (str): Short biography for user (Optional).
        avatar_url (str): URL avatar for user (Optional).
        updated_at (datetime): Datetime last update profile.
        user_id (int): ID of user associated with profile (One-To-One).
        country_id (int): ID of user country, linked to `Country` model.
        rank_id (int): ID of user rank, linked to `Rank` model. Default is None.

    Relationships:
        user (User): One-To-One relationship with `User` model.
        country (Country): One-To-Many relationship with the `Country` model.
        rank (Rank): One-To-Many relationship with the `Rank` model.

    """

    __tablename__ = "profiles"

    name: Mapped[Optional[str]] = mapped_column(String(25))
    surname: Mapped[Optional[str]] = mapped_column(String(35))
    gender: Mapped[ENUM] = mapped_column(
        ENUM("Male", "Female", "Not Defined", name="gender_enum"), default="Not Defined"
    )
    date_of_birth: Mapped[Optional[date]] = mapped_column()
    biography: Mapped[Optional[str]] = mapped_column(String(300))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )
    # One-To-One
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), unique=True)

    # One-To-Many
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    rank_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ranks.id"), default=None)

    # link to models
    user: Mapped["User"] = relationship(back_populates="profile")
    country: Mapped["Country"] = relationship(back_populates="profiles")
    rank: Mapped[Optional["Rank"]] = relationship(back_populates="profiles")

    def __repr__(self):
        return f"<Profile({self.user_id=}, {self.name if self.name else 'No name'})>"


class Country(Base):
    """Model country.

    Represents a country where user is located or associated with.

    Attributes:
        name (str): The name of the country. This is unique.
        code (str): The ISO 2-letter code of the country. This is unique.
        description (str): Optional description for country.

    Relationships:
        profiles (Profile): Many-To-One relationship with the `Profile` model,
        representing all users from this country.

    """

    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    code: Mapped[str] = mapped_column(String(2), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(300))

    # Link to 'Profile' model
    profiles: Mapped[Profile] = relationship(back_populates="country")

    def __repr__(self):
        return f"<Country({self.name} ({self.code}))>"


class Rank(Base):
    """Model rank.

    Represents title associated with user.

    Attributes:
        name (str): The name of rank (e.g., Grandmaster, International Master).
        acronym (str): The abbreviation for rank (e.g., GM, IM).
        description (str): Optional description for rank.

    Relationships:
        profiles (Profile): Many-To-One relationship with `Profile` model,
        representing all users with this rank.


    """

    __tablename__ = "ranks"

    name: Mapped[str] = mapped_column(String(30), unique=True)
    acronym: Mapped[str] = mapped_column(String(3), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(300))

    # Link to 'Profile' model
    profiles: Mapped[Profile] = relationship(back_populates="rank")

    def __repr__(self):
        return f"<Rank({self.name} ({self.acronym}))>"
