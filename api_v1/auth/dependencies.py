from typing import Annotated, Any

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_helper import db_helper

from .constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from .models import User
from .services import get_user_by_username
from .utils import check_password, decode_jwt

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login/")


def get_current_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict[str, Any]:
    """Get payload from token."""
    try:
        payload: dict = decode_jwt(token=token)

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    return payload


class UserGetterFromToken:
    """Class for get user from token."""

    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        session: Annotated[AsyncSession, Depends(db_helper.get_scoped_session)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
    ) -> User:
        """Retrieve user from database based on data from token."""
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_username(session, payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def validate_auth_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_scoped_session)],
    username: str = Form(),
    password: str = Form(),
) -> User:
    """Verify users authentificate by username and password."""
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )

    if not (user := await get_user_by_username(session, username)):
        raise unauth_exc

    if not check_password(raw_password=password, hash_password=user.password_hash):
        raise unauth_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )

    return user


def validate_token_type(payload: dict, token_type: str) -> bool:
    """Verify type token in payload."""
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_user_by_token_username(session: AsyncSession, payload: dict) -> User:
    """Retrieve user from database based on username from token."""
    username: str = payload.get("username", "")
    if user := await get_user_by_username(session=session, username=username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_active_auth_user(
    user: Annotated[User, Depends(get_current_auth_user)],
) -> User:
    """Get the current active user."""
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )
    return user
