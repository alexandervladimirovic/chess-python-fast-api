from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from utils import now_with_tz_utc


class DescriptionMixin(object):
    """Mixin for adding description field in tables."""

    _max_len_description_field = 300

    description: Mapped[Optional[str]] = mapped_column(
        String(_max_len_description_field)
    )


class TimestampMixin(object):
    """Mixin for adding created_at and updated_at fields in tables."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz_utc,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_with_tz_utc,
        server_default=func.now(),
        onupdate=now_with_tz_utc,
        server_onupdate=func.now(),
    )
