from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DatabaseHelper:
    """Class for creating async database connections using SQLAlchemy.

    Class allows you to create an async database connection using
    SQLAlchemy provides a session factory for working with transactions async.

    Attributes:
        engine (AsyncEngine): Async engine for connecting to database.
        session_factory (sessionmaker): Factory for creating async sessions.

    Methods:
        __init__(url: str, echo: bool = False): Constructor of
        class that initializes async engine and session factory.

    """

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        """Create and return a scoped session bound to the current async task.

        Returns:
            async_scoped_session: Scoped session tied to current async task.

        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """Async generator that provides database session for dependency injection.

        Yields:
            AsyncSession: The async database session.

        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(
        self,
    ) -> AsyncGenerator[async_scoped_session[AsyncSession], None]:
        """Async generator that provides scoped database session to current async task.

        Method creates scoped session that is tied to current async task
        using 'async_scoped_session'. The session is yield to the caller for usage in
        context of current task, and automatic closed after the task is
        completed.

        Yields:
        AsyncSession: An async database session bound to the current async task.

        """
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.postgres_db_url,
    echo=settings.db_echo,
)
