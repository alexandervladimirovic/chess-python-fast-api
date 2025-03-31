from datetime import datetime
from zoneinfo import ZoneInfo


def now_with_tz_utc():
    """Return datetime with timezone: UTC."""
    return datetime.now(tz=ZoneInfo("UTC"))
