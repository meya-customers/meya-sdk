import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_log_message_entry
from meya.element.element_test import frozen_milliseconds_timestamp
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.flow.component.set import FlowSetComponent
from meya.log.entry.message import LogMessageEntry
from meya.log.level import Level
from meya.log.scope import Scope


@pytest.mark.parametrize(
    ("flow_data", "flow_set", "expected_flow_data"),
    [
        (
            {"result": "test@meya.ai"},
            "email",
            {"result": "test@meya.ai", "email": "test@meya.ai"},
        ),
        (
            {"K1": "V1", "foo": "baz"},
            {"email": "test@meya.ai", "foo": "bar"},
            {"K1": "V1", "email": "test@meya.ai", "foo": "bar"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_flow_set_component(flow_data, flow_set, expected_flow_data):
    component = FlowSetComponent(flow_set=flow_set)
    component_start_entry = create_component_start_entry(
        component, data=flow_data
    )
    flow_next_entry = create_flow_next_entry(
        component_start_entry, data=expected_flow_data
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[flow_next_entry],
    )


@pytest.mark.asyncio
async def test_flow_set_component_no_result():
    """
    When `flow_set` is a string then the component expects the `result` key
    to be present in `flow_data` otherwise it logs and error.
    """
    flow_set = "email"
    component = FlowSetComponent(flow_set=flow_set)
    component_start_entry = create_component_start_entry(
        component, data={"K1": "V1"}
    )
    log_entry = create_log_message_entry(
        Level.ERROR,
        (
            f'Could not set flow scope property "{flow_set}"'
            f" because flow.result is not set"
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[log_entry],
    )
