import pytest

from meya.analytics.component.identify import IdentifyComponent
from meya.analytics.event.identify import IdentifyEvent
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from typing import Optional


@pytest.mark.parametrize(
    ("identify", "context", "timestamp"),
    [
        (dict(pi=3.14159, foo="bar"), {}, None),
        (dict(pi=3.14159, foo="bar"), dict(ip="127.0.0.1"), None),
        (dict(pi=3.14159, foo="bar"), dict(ip="127.0.0.1"), 1569957070.488),
    ],
)
@pytest.mark.asyncio
async def test_identify_component(
    identify: dict, context: dict, timestamp: Optional[float]
):
    component = IdentifyComponent(
        identify=identify, context=context, timestamp=timestamp
    )
    component_start_entry = create_component_start_entry(component)
    identify_event = IdentifyEvent(
        data=identify, context=context, timestamp=timestamp
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[identify_event, flow_next_entry],
    )
