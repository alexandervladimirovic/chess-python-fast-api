from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import (
    get_current_active_user,
    get_current_auth_user_for_refresh,
    http_bearer,
    validate_auth_user,
)
from .jwt_auth import create_access_token, create_refresh_token
from .models import User
from .schemas import TokenSchema

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/token/")
def auth_user_ussues_jwt(
    user: Annotated[User, Depends(validate_auth_user)],
) -> TokenSchema:
    """Authenticate user with username and password, and issue JWT.

    Endpoint takes users credentials (username and password), verify them,
    and return access token and refresh token for further authentication.
    """
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/users/me/")
def user_check_self_info(
    user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, str]:
    """Retrieve current authenticated users information.

    Endpoint return username and email of curren authenticated
    user.
    """
    return {
        "username": user.username,
        "email": user.email,
    }


@router.post("/refresh/", response_model_exclude_none=True)
def auth_refresh_jwt(
    user: Annotated[User, Depends(get_current_auth_user_for_refresh)],
) -> TokenSchema:
    """Refresh access token using valid refresh token.

    Endpoint allows user to obtain new access token using provided
    refresh token.
    """
    access_token = create_access_token(user)

    return TokenSchema(access_token=access_token)
