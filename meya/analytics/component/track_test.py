import pytest

from meya.analytics.component.track import TrackComponent
from meya.analytics.event.track import TrackEvent
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from typing import Optional


@pytest.mark.parametrize(
    ("track", "data", "context", "timestamp"),
    [
        ("custom_event_123", None, {}, None),
        ("custom_event_abc", dict(pi=3.14159, foo="bar"), {}, None),
        (
            "custom_event_DEF",
            dict(pi=3.14159, foo="bar"),
            dict(ip="127.0.0.1"),
            None,
        ),
        (
            "custom_event_456",
            dict(pi=3.14159, foo="bar"),
            dict(ip="127.0.0.1"),
            1569957070.488,
        ),
    ],
)
@pytest.mark.asyncio
async def test_track_component(
    track: str, data: Optional[dict], context: dict, timestamp: Optional[float]
):
    component = TrackComponent(
        track=track, data=data, context=context, timestamp=timestamp
    )
    component_start_entry = create_component_start_entry(component)
    track_event = TrackEvent(
        event=track, data=data, context=context, timestamp=timestamp
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[track_event, flow_next_entry],
    )
