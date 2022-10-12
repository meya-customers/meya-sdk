import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_log_message_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_thread_changes
from meya.element.element_test import verify_process_element
from meya.log.level import Level
from meya.thread.component.set import ThreadSetComponent
from typing import Union


@pytest.mark.parametrize(
    ("flow_data", "thread_set", "existing_thread_data", "thread_updates"),
    [
        ({"result": "test@meya.ai"}, "email", {}, {"email": "test@meya.ai"}),
        ({"result": "test@meya.ai"}, "email", {"email": "test@meya.ai"}, {}),
        (
            {},
            {"email": "test@meya.ai", "foo": "bar"},
            {},
            {"email": "test@meya.ai", "foo": "bar"},
        ),
        (
            {},
            {"email": "test@meya.ai", "foo": "bar"},
            {"foo": "bar"},
            {"email": "test@meya.ai"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_thread_set_component(
    flow_data: dict,
    thread_set: Union[str, dict],
    existing_thread_data: dict,
    thread_updates: dict,
):
    thread = create_thread(data=existing_thread_data)
    component = ThreadSetComponent(thread_set=thread_set)
    component_start_entry = create_component_start_entry(
        component, thread=thread, data=flow_data
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    thread_changes = create_thread_changes(thread, thread_updates)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[flow_next_entry, *thread_changes],
        thread=thread,
    )


@pytest.mark.asyncio
async def test_thread_set_component_no_result():
    """
    When `thread_set` is a string then the component expects the `result` key
    to be present in `flow_data` otherwise it logs and error.
    """
    thread_set = "email"
    component = ThreadSetComponent(thread_set=thread_set)
    component_start_entry = create_component_start_entry(
        component, data={"K1": "V1"}
    )
    log_entry = create_log_message_entry(
        Level.ERROR,
        (
            f'Could not set thread scope property "{thread_set}"'
            f" because flow.result is not set"
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[log_entry],
    )
