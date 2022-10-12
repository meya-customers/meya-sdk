import pytest

from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import verify_process_element
from meya.flow.component.next import NextComponent


@pytest.mark.parametrize(
    ("flow_data", "next_data", "expected_flow_data"),
    [
        ({"result": "test@meya.ai"}, None, {"result": "test@meya.ai"}),
        (
            {"K1": "V1", "foo": "baz"},
            {"email": "test@meya.ai", "foo": "bar"},
            {"K1": "V1", "email": "test@meya.ai", "foo": "bar"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_flow_set_component(flow_data, next_data, expected_flow_data):
    bot = create_bot()
    thread = create_thread()
    component = NextComponent(next=next_data)
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread, data=flow_data
    )
    flow_next_entry = create_flow_next_entry(
        component_start_entry, data=expected_flow_data
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[flow_next_entry],
        thread=thread,
        extra_elements=[bot],
    )
