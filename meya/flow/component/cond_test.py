import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.cond import CondComponent
from meya.flow.component.jump import JumpComponent
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.util.dict import to_dict
from typing import Any


@pytest.mark.parametrize(
    ("value", "label"),
    [("a", "l0"), ("b", "l1"), ("c", "l2"), ("d", "l3"), ("e", "l3")],
)
@pytest.mark.asyncio
async def test_case_component_jump(value: Any, label: str):
    bot = create_bot()
    thread = create_thread()
    flow = "flow"
    data = {"K1": "V2"}
    stack = []

    def jump(label: str):
        return to_spec(
            JumpComponent(jump=StepLabelRef(label), context_flow=FlowRef(flow))
        )

    component = CondComponent(
        cond=[
            {value <= "a": jump("l0")},
            {value <= "b": jump("l1")},
            {value <= "c": jump("l2")},
            {value == "f": jump("l4")},
        ],
        default=jump("l3"),
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
    jump_entry = ComponentStartEntry(
        bot_id=bot.id,
        data=data,
        flow=flow,
        index=0,
        spec=to_dict(jump(label)),
        stack=stack,
        thread_id=thread.id,
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[jump_entry],
        thread=thread,
        extra_elements=[bot],
    )
