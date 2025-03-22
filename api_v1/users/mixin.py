from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class DescriptionMixin(object):
    """Mixin for adding description field."""

    _max_len_description_field = 300

    description: Mapped[Optional[str]] = mapped_column(
        String(_max_len_description_field)
    )
