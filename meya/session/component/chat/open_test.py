import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.session.component.chat.open import ChatOpenComponent
from meya.session.event.chat.open import ChatOpenEvent


@pytest.mark.asyncio
async def test_open_chat_component():
    component = ChatOpenComponent()
    component_start_entry = create_component_start_entry(component)
    open_chat_event = ChatOpenEvent()
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[open_chat_event, flow_next_entry],
    )
