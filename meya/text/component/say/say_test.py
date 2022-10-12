import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent


@pytest.mark.asyncio
async def test_say_component():
    component = SayComponent(say="Hello, world!")
    component_start_entry = create_component_start_entry(component)
    say_event = SayEvent(text="Hello, world!")
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[say_event, flow_next_entry],
    )
