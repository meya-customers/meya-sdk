import re

from datetime import timedelta

UNITS = dict(
    w=timedelta(weeks=1),
    d=timedelta(days=1),
    h=timedelta(hours=1),
    m=timedelta(minutes=1),
    s=timedelta(seconds=1),
    ms=timedelta(milliseconds=1),
    us=timedelta(microseconds=1),
)

ZERO_UNIT_NAME = "s"

LAST_UNIT_NAME = list(UNITS.keys())[-1]

PARSER = re.compile(
    r"""
    (?P<amount>[0-9]+(?:\.[0-9]+)?)
    (?P<unit>[a-z]+)
""",
    flags=re.VERBOSE,
)


def from_timedelta(obj: timedelta) -> str:
    if obj == timedelta():
        return f"0{ZERO_UNIT_NAME}"

    if obj < timedelta():
        negative = True
        obj = -obj
    else:
        negative = False

    result = []

    for unit_name in UNITS:
        unit = UNITS[unit_name]

        if unit_name != LAST_UNIT_NAME:
            part, obj = divmod(obj, unit)
        else:
            part = obj // unit

        if part > 0:
            result.append(f"{part}{unit_name}")

    result = " ".join(result)
    if negative:
        return f"-{result}"
    else:
        return result


def to_timedelta(data: str) -> timedelta:
    if data.startswith("-"):
        negative = True
        data = data[1:]
    else:
        negative = False

    error = False
    result = timedelta()

    for part in data.split(" "):
        match_result = PARSER.fullmatch(part)
        if not match_result:
            error = True
            break
        groups = match_result.groupdict()
        unit = UNITS.get(groups["unit"])
        if not unit:
            error = True
            break
        amount = float(groups["amount"])
        result += amount * unit

    if error:
        raise ValueError(f'"{data}" is not a valid timedelta')
    elif negative:
        return -result
    else:
        return result
