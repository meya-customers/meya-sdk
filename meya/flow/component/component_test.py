import pytest

from meya.bot.element import BotRef
from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component import FlowComponent
from meya.flow.element import Flow
from meya.flow.element import FlowRef
from meya.flow.element import StepLabel
from meya.flow.element import StepLabelRef
from meya.flow.entry.start import FlowStartEntry
from meya.flow.stack_frame import StackFrame
from meya.text.component.say import SayComponent
from typing import List
from typing import Optional


@pytest.mark.parametrize(("label",), [(None,), ("h1",), (" h2 ",)])
@pytest.mark.parametrize(("flow",), [("flow123",), ("flow_abc",)])
@pytest.mark.parametrize(
    ("data",), [(None,), ({"K1": "V2", "K3": "V4"},), ({},)]
)
@pytest.mark.parametrize(
    ("parent_flow", "parent_data", "parent_index", "parent_stack"),
    [
        ("f1", {}, 0, []),
        (
            "f2",
            {"K1": "V1"},
            1,
            [
                StackFrame(data={}, flow="f1", index=1),
                StackFrame(data={"K1": "V0"}, flow="f1", index=1),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_flow_component_normal(
    label: Optional[str],
    flow: str,
    data: Optional[dict],
    parent_flow: str,
    parent_data: dict,
    parent_index: int,
    parent_stack: List[StackFrame],
):
    bot = create_bot()
    thread = create_thread()
    flow_ref = FlowRef(flow)
    flow_element = Flow(
        id=flow,
        steps=[StepLabel(label.strip()), to_spec(SayComponent(say="hi"))]
        if label
        else [to_spec(SayComponent(say="hi"))],
    )
    component = FlowComponent(
        flow=flow_ref, jump=StepLabelRef(label) if label else None, data=data
    )
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        data=parent_data,
        flow=parent_flow,
        index=parent_index,
        spec=to_spec_dict(component),
        stack=parent_stack,
        thread_id=thread.id,
    )
    start_entry = FlowStartEntry(
        bot_id=bot.id,
        data=data or {},
        flow=flow.strip(),
        label=label and label.strip(),
        stack=[
            StackFrame(data=parent_data, flow=parent_flow, index=parent_index),
            *parent_stack,
        ],
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[start_entry],
        thread=thread,
        extra_elements=[bot, flow_element],
    )


@pytest.mark.parametrize(("label",), [(None,), ("h1",), (" h2 ",)])
@pytest.mark.parametrize(("flow",), [("flow123",), ("flow_abc",)])
@pytest.mark.parametrize(
    ("data",), [(None,), ({"K1": "V2", "K3": "V4"},), ({},)]
)
@pytest.mark.parametrize(
    ("parent_flow", "parent_data", "parent_index", "parent_stack"),
    [
        ("f1", {}, 0, []),
        (
            "f2",
            {"K1": "V1"},
            1,
            [
                StackFrame(data={}, flow="f1", index=1),
                StackFrame(data={"K1": "V0"}, flow="f1", index=1),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_flow_component_transfer(
    label: Optional[str],
    flow: str,
    data: Optional[dict],
    parent_flow: str,
    parent_data: dict,
    parent_index: int,
    parent_stack: List[StackFrame],
):
    bot = create_bot()
    thread = create_thread()
    flow_ref = FlowRef(flow)
    flow_element = Flow(
        id=flow,
        steps=[StepLabel(label.strip()), to_spec(SayComponent(say="hi"))]
        if label
        else [to_spec(SayComponent(say="hi"))],
    )
    component = FlowComponent(
        flow=flow_ref,
        jump=StepLabelRef(label) if label else None,
        data=data,
        transfer=True,
    )
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        data=parent_data,
        flow=parent_flow,
        index=parent_index,
        spec=to_spec_dict(component),
        stack=parent_stack,
        thread_id=thread.id,
    )
    start_entry = FlowStartEntry(
        bot_id=bot.id,
        data=data or {},
        flow=flow.strip(),
        label=label and label.strip(),
        stack=parent_stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[start_entry],
        thread=thread,
        extra_elements=[bot, flow_element],
    )


@pytest.mark.parametrize(("label",), [(None,), ("h1",), (" h2 ",)])
@pytest.mark.parametrize(("flow",), [("flow123",), ("flow_abc",)])
@pytest.mark.parametrize(
    ("data",), [(None,), ({"K1": "V2", "K3": "V4"},), ({},)]
)
@pytest.mark.parametrize(
    ("parent_flow", "parent_data", "parent_index", "parent_stack"),
    [
        ("f1", {}, 0, []),
        (
            "f2",
            {"K1": "V1"},
            1,
            [
                StackFrame(data={}, flow="f1", index=1),
                StackFrame(data={"K1": "V0"}, flow="f1", index=1),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_flow_component_async(
    label: Optional[str],
    flow: str,
    data: Optional[dict],
    parent_flow: str,
    parent_data: dict,
    parent_index: int,
    parent_stack: List[StackFrame],
):
    bot = create_bot()
    other_bot = create_bot()
    thread = create_thread()
    other_thread = create_thread()
    flow_ref = FlowRef(flow)
    flow_element = Flow(
        id=flow,
        steps=[StepLabel(label.strip()), to_spec(SayComponent(say="hi"))]
        if label
        else [to_spec(SayComponent(say="hi"))],
    )
    component = FlowComponent(
        flow=flow_ref,
        jump=StepLabelRef(label) if label else None,
        data=data,
        async_=True,
        bot=BotRef(other_bot.id),
        thread_id=other_thread.id,
    )
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        data=parent_data,
        flow=parent_flow,
        index=parent_index,
        spec=to_spec_dict(component),
        stack=parent_stack,
        thread_id=thread.id,
    )
    start_entry = FlowStartEntry(
        bot_id=other_bot.id,
        data=data or {},
        flow=flow.strip(),
        label=label and label.strip(),
        stack=[],
        thread_id=other_thread.id,
    )
    next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[start_entry, next_entry],
        thread=thread,
        extra_elements=[bot, other_bot, flow_element],
    )
