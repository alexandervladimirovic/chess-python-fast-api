from datetime import timedelta

from core.config import settings

from .constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from .models import User
from .utils import encode_jwt


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.jwt.access_token_expires_in_minutes,
    expire_timedelta: timedelta | None = None,
):
    """Create  JWT with data and lifetime.

    Args:
        token_type (str): type token (ex. `access`, `refresh` and etc).
        token_data (dict): Data that will be included in token.
        expire_minutes (int): Lifetime of token in minutes.
        expire_timedelta (timedelta, Optional): Lifetime of token in form of timedelta
        (overrides expire_minutes if passed).

    Returns:
        JWT encoded in form of string.


    """
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User):
    """Create access JWT for users.

    Args:
        user (UserLoginSchema): Data schema of user for whom the token is being created.

    Returns:
        Access JWT.

    """
    payload = {
        "sub": str(user.uuid),
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.jwt.access_token_expires_in_minutes,
    )


def create_refresh_token(user: User):
    """Create refresh JWT for users.

    Args:
        user (UserLoginSchema): Data schema of user for whom the token is being created.

    Returns:
        Refresh JWT.

    """
    payload = {"sub": str(user.uuid), "username": user.username}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.jwt.refresh_token_expires_in_days),
    )
