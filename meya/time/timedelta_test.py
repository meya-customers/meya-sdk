import pytest

from datetime import timedelta
from meya.time.timedelta import from_timedelta
from meya.time.timedelta import to_timedelta
from typing import Optional


@pytest.mark.parametrize(
    ("obj", "data"), [(timedelta(milliseconds=1.1234567), "1ms 123us")]
)
def test_format(obj: timedelta, data: str):
    assert from_timedelta(obj) == data


@pytest.mark.parametrize(
    ("obj", "data"),
    [
        (timedelta(microseconds=1123), "1.1234567ms"),
        (timedelta(seconds=61), "61s"),
        (timedelta(), "0d"),
        (None, ""),
        (None, "x"),
        (None, "1s "),
        (None, " 1s"),
        (None, "1.1.1s"),
    ],
)
def test_parse(obj: Optional[timedelta], data: str):
    if obj is not None:
        assert to_timedelta(data) == obj
    else:
        with pytest.raises(ValueError):
            to_timedelta(data)


@pytest.mark.parametrize(
    ("obj", "data"),
    [
        (timedelta(minutes=1, seconds=1), "1m 1s"),
        (-timedelta(days=2, milliseconds=5), "-2d 5ms"),
        (timedelta(seconds=1.01), "1s 10ms"),
        (timedelta(), "0s"),
    ],
)
def test_round_trip(obj: timedelta, data: str):
    assert to_timedelta(data) == obj
    assert from_timedelta(obj) == data

    result = from_timedelta(to_timedelta(data))
    assert result == data

    result = to_timedelta(from_timedelta(obj))
    assert result == obj
