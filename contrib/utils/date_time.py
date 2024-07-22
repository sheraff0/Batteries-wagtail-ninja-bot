import re
from functools import wraps
import inspect
from pytz import timezone
from datetime import date, datetime, timedelta
import time

from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from zoneinfo import ZoneInfo


def validate_timezone(value):
    try:
        assert ZoneInfo(value)
    except:
        raise ValidationError("Invalid timezone!")


def naive_to_utc(datetime_string):
    try:
        if not any((
            re.search("Z$", datetime_string),
            re.search("\+[\d:]+$", datetime_string),
        )):
            return datetime_string + "Z"
    except: ...
    return datetime_string


def get_timestamp():
    return int(localtime().timestamp())


def timeit(func):
    def print_time(t0):
        delta = round((time.time() - t0) * 1000, 2)
        print("Performed {2}{0}{4} in {3}{1} ms{4}".format(func.__name__, delta,
            "\033[96m\033[3m", "\033[93m\033[3m", "\033[0m" ), flush=True)

    def _(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        print_time(t0)
        return result

    async def _a(*args, **kwargs):
        t0 = time.time()
        result = await func(*args, **kwargs)
        print_time(t0)
        return result
    return _a if inspect.iscoroutinefunction(func) else _


def get_local_datetime(zone: str):
    _tz = timezone(zone)
    return datetime.now().astimezone(_tz)


def get_today(offset=0):
    return datetime.now().date() + timedelta(days=offset)


def get_yesterday():
    return get_today(-1)


def get_tomorrow():
    return get_today(1)


def localdate():
    return now().today().date()


def str_to_date(value, default=None):
    try:
        return date(*map(int, value.split("-")))
    except:
        return default


def start_date(value):
    return str_to_date(value, default=date(1900, 1, 1))


def end_date(value):
    return str_to_date(value, default=date(2100, 1, 1))


def get_date_interval(obj):
    _map = (
        ("start", "с"),
        ("end", "по"),
    )
    return " ".join(
        f"{prefix} {_value}"
        for key, prefix in _map
        if (_value := obj.get(key))
    )
