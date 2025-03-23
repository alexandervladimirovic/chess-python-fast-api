from datetime import datetime
from typing import Optional

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column


class DescriptionMixin(object):
    """Mixin for adding description field in tables."""

    _max_len_description_field = 300

    description: Mapped[Optional[str]] = mapped_column(
        String(_max_len_description_field)
    )


class TimestampMixin(object):
    """Mixin for adding created_at and updated_at fields in tables."""

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
        onupdate=datetime.now,
        server_onupdate=func.now(),
    )
