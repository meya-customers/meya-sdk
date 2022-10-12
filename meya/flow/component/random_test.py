import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.jump import JumpComponent
from meya.flow.component.random import RandomComponent
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.util.dict import to_dict
from unittest.mock import patch


@pytest.mark.asyncio
async def test_random_component_jump():
    bot = create_bot()
    thread = create_thread()
    label = "l2"
    flow = "flow"
    data = {"K1": "V2"}
    stack = []

    def jump(label: str):
        return to_spec(
            JumpComponent(jump=StepLabelRef(label), context_flow=FlowRef(flow))
        )

    component = RandomComponent(
        random=[jump("l0"), jump("l1"), jump("l2"), jump("l3")]
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
    with patch(new=lambda seq: seq[2], target="random.choice"):
        await verify_process_element(
            element=component,
            sub_entry=component_start_entry,
            expected_pub_entries=[jump_entry],
            thread=thread,
            extra_elements=[bot],
        )
