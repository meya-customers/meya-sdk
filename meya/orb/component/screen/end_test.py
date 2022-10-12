import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.orb.component.screen.end import ScreenEndComponent
from meya.orb.event.screen.end import ScreenEndEvent


@pytest.mark.asyncio
async def test_screen_end_component():
    component = ScreenEndComponent()
    component_start_entry = create_component_start_entry(component)
    screen_end_event = ScreenEndEvent()
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[screen_end_event, flow_next_entry],
    )
