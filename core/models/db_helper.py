from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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


db_helper = DatabaseHelper(
    url=settings.postgres_db_url,
    echo=settings.db_echo,
)
