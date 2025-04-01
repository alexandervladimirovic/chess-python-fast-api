from __future__ import annotations

import re
from typing import Any, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator,
)

from schemas import ChessBaseSchema

from .exceptions import (
    InvalidUsernameCharacherError,
    NoWhitespaceInPasswordError,
    PasswordNoDigitError,
    PasswordNotEqualError,
    PasswordNoUpperAndLowerCharError,
    PasswordShortLengthError,
    UsernameOrEmailRequiredError,
    UsernameTooShortError,
)
from .utils import hash_password


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

    username: str
    email: EmailStr
    password: str
    confirm_password: str
    # profile: ProfileSchema
    # roles: list[RolesSchema]

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        """Validate username for complexity and allowed characters."""
        if len(username) < 6:
            raise UsernameTooShortError
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise InvalidUsernameCharacherError
        return username

    @model_validator(mode="before")
    @classmethod
    def validate_password_confirmation(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Method for confirm password."""
        if values.get("password") != values.get("confirm_password"):
            raise PasswordNotEqualError
        return values

    @field_validator("password", mode="before")
    @classmethod
    def validate_and_hash_password(cls, password: str):
        """Check password complexity and return hashed password."""
        if not password or len(password) < 8:
            raise PasswordShortLengthError
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


class TokenSchemas(BaseModel):
    """Schema for representing a token response."""

    token: str
    token_type: str
