import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.session.component.chat.close import ChatCloseComponent
from meya.session.event.chat.close import ChatCloseEvent


@pytest.mark.asyncio
async def test_close_chat_component():
    component = ChatCloseComponent()
    component_start_entry = create_component_start_entry(component)
    close_chat_event = ChatCloseEvent()
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[close_chat_event, flow_next_entry],
    )
