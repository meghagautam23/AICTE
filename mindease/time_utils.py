from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import current_app


def get_app_timezone():
    timezone_name = current_app.config.get("APP_TIMEZONE", "Asia/Kolkata")
    try:
        return ZoneInfo(timezone_name)
    except Exception:
        return timezone.utc


def to_local(dt_value):
    if dt_value is None:
        return None

    # Datetimes in DB are stored as UTC-naive, so attach UTC before converting.
    if dt_value.tzinfo is None:
        dt_value = dt_value.replace(tzinfo=timezone.utc)
    else:
        dt_value = dt_value.astimezone(timezone.utc)

    return dt_value.astimezone(get_app_timezone())


def format_local(dt_value, fmt="%d %b %Y, %I:%M %p"):
    local_dt = to_local(dt_value)
    return local_dt.strftime(fmt) if local_dt else ""


def local_now():
    return datetime.now(get_app_timezone())
