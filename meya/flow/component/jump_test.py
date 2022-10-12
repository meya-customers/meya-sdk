import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.jump import JumpComponent
from meya.flow.element import Flow
from meya.flow.element import FlowRef
from meya.flow.element import StepLabel
from meya.flow.element import StepLabelRef
from meya.flow.entry.jump import FlowJumpEntry
from meya.flow.stack_frame import StackFrame
from meya.text.component.say import SayComponent


@pytest.mark.parametrize(
    ("label", "flow", "data"),
    [
        ("h1", "flow123", {"K1": "V2", "K3": "V4"}),
        ("hello", "flow_abc", {}),
        ("done", "f1", {"foo": "bar"}),
        ("error", "f1", {}),
        (" \nwhitespace\n", "f1", {}),
    ],
)
@pytest.mark.asyncio
async def test_jump_component_no_data(label: str, flow: str, data: dict):
    bot = create_bot()
    thread = create_thread()
    stack = [StackFrame(data={"a": 1}, flow="f1", index=2)]
    flow_ref = FlowRef(flow)
    flow_element = Flow(
        id=flow_ref.ref,
        steps=[StepLabel(label.strip()), to_spec(SayComponent(say="hi"))],
    )
    component = JumpComponent(jump=StepLabelRef(label), context_flow=flow_ref)
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        spec=to_spec_dict(component),
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    jump_entry = FlowJumpEntry(
        bot_id=bot.id,
        data=data,
        flow=flow,
        label=label.strip(),
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[jump_entry],
        thread=thread,
        extra_elements=[bot, flow_element],
    )


@pytest.mark.asyncio
async def test_jump_component_with_data():
    bot = create_bot()
    thread = create_thread()
    label = "l1"
    flow = "f1"
    data = {"K0": "V0", "K1": "V1"}
    stack = [StackFrame(data={"a": 1}, flow="f1", index=2)]
    flow_ref = FlowRef(flow)
    flow_element = Flow(
        id=flow_ref.ref,
        steps=[StepLabel(label.strip()), to_spec(SayComponent(say="hi"))],
    )
    component = JumpComponent(
        jump=StepLabelRef(label),
        data={"K1": "V2", "K2": "V3"},
        context_flow=FlowRef(flow),
    )
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        spec=to_spec_dict(component),
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    jump_entry = FlowJumpEntry(
        bot_id=bot.id,
        data={"K0": "V0", "K1": "V2", "K2": "V3"},
        flow=flow,
        label=label,
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[jump_entry],
        thread=thread,
        extra_elements=[bot, flow_element],
    )
