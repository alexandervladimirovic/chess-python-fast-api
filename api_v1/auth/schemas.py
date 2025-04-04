from __future__ import annotations

import re
from datetime import date
from typing import Any, Optional

from pydantic import (
    EmailStr,
    Field,
    HttpUrl,
    PositiveInt,
    field_validator,
    model_validator,
)

from schemas import ChessBaseSchema

from .enums import GenderEnum
from .exceptions import (
    DateOfBirthFutureError,
    DateOfBirthMinAgeError,
    InvalidUsernameCharacherError,
    NoWhitespaceInPasswordError,
    PasswordNoDigitError,
    PasswordNoUpperAndLowerCharError,
    PasswordsNotEqualError,
    ProfileNameOrSurnameInvalidCharacherError,
    ProfileNameOrSurnameNoWhitespaceError,
    UsernameOrEmailRequiredError,
)
from .utils import hash_password

MIN_AGE = 3


class UserLoginSchema(ChessBaseSchema):
    """Schema for user login.

    This schema describes fields for entering username or email and password.
    Check performed for presence of least one of the fields: username or email.
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    @model_validator(mode="before")
    @classmethod
    def check_username_or_email(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Checking for username or email."""
        if not values.get("username") and not values.get("email"):
            raise UsernameOrEmailRequiredError
        return values


class UserRegisterSchema(ChessBaseSchema):
    """Schema for user registration.

    Schema describes fields for registration: username, email, password, and
    password confirmation.
    It includes checks for validating username and password, as well checking
    for password match and its confirmation.
    """

    username: str = Field(min_length=6, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str
    is_active: bool = True
    # roles: list[RolesSchema]

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        """Validate username for complexity and allowed characters."""
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise InvalidUsernameCharacherError
        return username

    @model_validator(mode="before")
    @classmethod
    def validate_password_confirmation(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Method for confirm password."""
        if values.get("password") != values.get("confirm_password"):
            raise PasswordsNotEqualError
        return values

    @field_validator("password", mode="before")
    @classmethod
    def validate_and_hash_password(cls, password: str):
        """Check password complexity and return hashed password."""
        if not any(char.isdigit() for char in password):
            raise PasswordNoDigitError
        if not (
            any(char.isupper() for char in password)
            and any(char.islower() for char in password)
        ):
            raise PasswordNoUpperAndLowerCharError
        if " " in password:
            raise NoWhitespaceInPasswordError
        return hash_password(password)


class ProfileCreateSchema(ChessBaseSchema):
    """Schema for create user profile.

    Schema describes fields required to create a user profile:
    name, surname, gender, date of birth, biography, avatar URL, and foreign keys.
    """

    name: str | None = Field(min_length=2, max_length=30, default=None)
    surname: str | None = Field(min_length=4, max_length=40, default=None)
    gender: GenderEnum | None = GenderEnum.NOT_DEFINED
    date_of_birth: date | None = None
    biography: str | None = Field(max_length=300, default=None)
    avatar_url: HttpUrl | None = Field(max_length=255, default=None)

    user_id: PositiveInt
    country_id: PositiveInt
    rank_id: PositiveInt | None = None

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name: str) -> str | None:
        """Validate users name to ensure it contain no spaces and allowed char.

        Returns:
            Optional[str]: Validate name, properly capitalized.

        """
        if not name:
            return None
        if " " in name:
            raise ProfileNameOrSurnameNoWhitespaceError
        if not re.match(r"^[a-zA-Z-]+$", name):
            raise ProfileNameOrSurnameInvalidCharacherError
        return name.title()

    @field_validator("surname", mode="before")
    @classmethod
    def validate_surname(cls, surname: str) -> str | None:
        """Validate users surname to ensure it contain no spaces and allowed char.

        Returns:
            Optional[str]: Validate surname, properly capitalized.

        """
        if not surname:
            return None
        if " " in surname:
            raise ProfileNameOrSurnameNoWhitespaceError
        if not re.match(r"^[a-zA-Z-]+$", surname):
            raise ProfileNameOrSurnameInvalidCharacherError
        return surname.title()

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> date | None:
        """Validate date of birth.

        Validate users date of birth to ensure it's not in future
        and that user meets min age requirement.

        Returns:
            Optional[date]: The validated date of birth.

        """
        if not date_of_birth:
            return None

        today = date.today()

        if date_of_birth > today:
            raise DateOfBirthFutureError

        age = today.year - date_of_birth.year
        if today.month < date_of_birth.month or (
            today.month == date_of_birth.month and today.day < date_of_birth.day
        ):
            age -= 1

        if age < MIN_AGE:
            raise DateOfBirthMinAgeError

        return date_of_birth


class TokenSchema(ChessBaseSchema):
    """Schema for representing a token response."""

    token: str
    token_type: str
