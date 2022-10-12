import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.end import EndComponent
from meya.flow.entry.end import FlowEndEntry
from meya.flow.entry.next import FlowNextEntry
from meya.flow.stack_frame import StackFrame


@pytest.mark.asyncio
async def test_end_component_noop():
    bot = create_bot()
    thread = create_thread()
    flow = "flow"
    data = {"K1": "V2", "K3": "V4"}
    stack = []
    component = EndComponent(end=data)
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        spec=to_spec_dict(component),
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    end_entry = FlowEndEntry(
        bot_id=bot.id,
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[end_entry],
        thread=thread,
        extra_elements=[bot],
    )


@pytest.mark.asyncio
async def test_end_component_merge():
    bot = create_bot()
    thread = create_thread()
    flow = "flow"
    data = {"K1": "V2", "K3": "V4"}
    stack = [
        StackFrame(data={"K1": "V0", "K5": "V7"}, flow="f1", index=1),
        StackFrame(data={"K1": "V0", "K5": "V6"}, flow="f2", index=0),
    ]
    component = EndComponent(end=data)
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        spec=to_spec_dict(component),
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    next_entry = FlowNextEntry(
        bot_id=bot.id,
        data={"K1": "V2", "K3": "V4", "K5": "V7"},
        flow="f1",
        index=1,
        stack=stack[1:],
        thread_id=thread.id,
    )
    end_entry = FlowEndEntry(
        bot_id=bot.id,
        data=data,
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[next_entry, end_entry],
        thread=thread,
        extra_elements=[bot],
    )


@pytest.mark.asyncio
async def test_end_component_keep():
    bot = create_bot()
    thread = create_thread()
    flow = "flow"
    data = None
    stack = [
        StackFrame(data={"K1": "V0", "K5": "V7"}, flow="f1", index=1),
        StackFrame(data={"K1": "V0", "K5": "V6"}, flow="f2", index=0),
    ]
    component = EndComponent(end=data)
    component_start_entry = ComponentStartEntry(
        bot_id=bot.id,
        spec=to_spec_dict(component),
        data={},
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    next_entry = FlowNextEntry(
        bot_id=bot.id,
        data={"K1": "V0", "K5": "V7"},
        flow="f1",
        index=1,
        stack=stack[1:],
        thread_id=thread.id,
    )
    end_entry = FlowEndEntry(
        bot_id=bot.id,
        data={},
        flow=flow,
        index=0,
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[next_entry, end_entry],
        thread=thread,
        extra_elements=[bot],
    )
