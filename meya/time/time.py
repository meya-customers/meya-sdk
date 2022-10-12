import pytz

from datetime import datetime
from meya.util.enum import SimpleEnum
from numbers import Real
from time import perf_counter
from time import process_time
from time import time

Timezone = SimpleEnum(
    "Timezone",
    {
        timezone.upper().replace("/", "_"): timezone
        for timezone in pytz.all_timezones
    },
)


def get_milliseconds_timestamp() -> int:
    return int(time() * 1000)


def get_seconds_timestamp() -> int:
    return int(time())


def get_milliseconds_perf_counter() -> float:
    return perf_counter() * 1000


def get_milliseconds_process_time() -> float:
    return process_time() * 1000


def from_utc_milliseconds_timestamp(ts: Real) -> datetime:
    return from_utc_seconds_timestamp(ts / 1000.0)


def from_utc_seconds_timestamp(ts: Real) -> datetime:
    return datetime.utcfromtimestamp(float(ts)).replace(tzinfo=pytz.utc)


def to_utc_milliseconds_timestamp(ts: datetime) -> int:
    return int(ts.timestamp() * 1000)


def utcnow() -> datetime:
    return datetime.utcnow().astimezone(pytz.utc)
