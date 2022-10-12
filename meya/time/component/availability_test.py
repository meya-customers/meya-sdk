import pytest
import pytz

from datetime import datetime
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.time import Timezone
from meya.time.component.availability import TimeAvailabilityComponent
from typing import Optional


@pytest.mark.parametrize(
    ("timezone", "mon", "tue", "wed", "thu", "fri", "sat", "sun", "now", "ok"),
    [
        (None, None, None, None, None, None, None, None, None, False),
        (
            Timezone.AMERICA_TORONTO,
            "9-17",
            "9-12, 13-17",
            "9-17",
            "9-12, 13-17",
            "9-17",
            None,
            None,
            "2019-11-05 15:05:01.123456-05:00",
            True,
        ),
        (
            Timezone.AMERICA_TORONTO,
            "9-17",
            "9-12, 13-17",
            "9-17",
            "9-12, 13-17",
            "9-17",
            None,
            None,
            "2019-11-05 17:05:01.123456-05:00",
            False,
        ),
        (
            Timezone.AMERICA_TORONTO,
            "9-17",
            "9-12, 13-17",
            "9-17",
            "9-12, 13-17",
            "9-17",
            None,
            None,
            "2019-11-09 15:05:01.123456-05:00",
            False,
        ),
        (
            Timezone.AMERICA_TORONTO,
            "9-17",
            "9-12, 13-17",
            "9-17",
            "9-12, 13-17",
            "9-17",
            None,
            None,
            "2019-11-05 12:05:01.123456-05:00",
            False,
        ),
    ],
)
@pytest.mark.asyncio
async def test_time_availability_component(
    timezone: str,
    mon: Optional[str],
    tue: Optional[str],
    wed: Optional[str],
    thu: Optional[str],
    fri: Optional[str],
    sat: Optional[str],
    sun: Optional[str],
    now: str,
    ok: bool,
):
    if now:
        now = datetime.fromisoformat(now).astimezone(tz=pytz.utc)
    else:
        now = datetime.utcnow()
    kwargs = dict(
        mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, sun=sun
    )
    if timezone:
        kwargs["timezone"] = timezone
    component = TimeAvailabilityComponent(**kwargs)
    component_start_entry = create_component_start_entry(component)
    flow_next_entry = create_flow_next_entry(
        component_start_entry, data=dict(ok=ok)
    )
    await verify_process_element(
        component,
        component_start_entry,
        expected_pub_entries=[flow_next_entry],
        time_to_freeze=now,
    )
