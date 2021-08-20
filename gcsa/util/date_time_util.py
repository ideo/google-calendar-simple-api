from datetime import datetime, date, timedelta

import pytz
from tzlocal import get_localzone


def insure_localisation(dt, timezone=str(get_localzone())):
    """Insures localisation with provided timezone on "datetime" object.

    Does nothing to object of type "date"."""

    if isinstance(dt, datetime):
        try:
            tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            timezone = tz_from_offset(timezone)
            tz = pytz.timezone(timezone)

        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt
    elif isinstance(dt, date):
        return dt
    else:
        raise TypeError('"date" or "datetime" object expected, not {!r}.'.format(dt.__class__.__name__))


# RC NEW: Having trouble when something is returned as an offset instead of timezone
# So need to handle that
# Code adapted from https://stackoverflow.com/questions/35085289/getting-timezone-name-from-utc-offset

def tz_from_offset(offset_str):
    # utc_offset = timedelta(hours=5, minutes=30)  # +5:30
    is_positive = offset_str.find('+') > 0

    if is_positive:
        hours, minutes = [int(i) for i in offset_str.split('+')[1].split(':')]
        utc_offset = timedelta(hours=hours, minutes=minutes)
    else:
        hours, minutes = [int(i) for i in offset_str.split('-')[1].split(':')]
        utc_offset = timedelta(hours=-hours, minutes=minutes)

    now = datetime.now(pytz.utc)  # current time
    found = [
        tz.zone for tz
        in map(pytz.timezone, pytz.common_timezones_set)
        if now.astimezone(tz).utcoffset() == utc_offset
    ]
    return found[0]
