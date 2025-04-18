from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Abstract base class for SQLAlchemy models.

    This class provides common functionality for all models
    using SQLAlchemy, and defines the standard `id` field, which
    it will be used as the primary key for each model.

    Attributes:
        id (int): Unique ID of the record, autoincrement
                  and being primary key for other model.

    """

    __abstract__ = True
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
