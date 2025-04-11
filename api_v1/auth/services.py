from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserRegisterSchema


async def create_user(session: AsyncSession, user_in: UserRegisterSchema) -> User:
    """Create new user in database."""
    data = user_in.model_dump(exclude={"confirm_password"}, by_alias=True)

    user = User(**data)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        raise


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    """Search user by username in database."""
    stmt = select(User).where(User.username == username)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    return user
