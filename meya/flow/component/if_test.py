import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.if_ import IfComponent
from meya.flow.component.jump import JumpComponent
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.util.dict import to_dict
from typing import Any


@pytest.mark.parametrize(
    ("condition", "label", "jump_data"),
    [
        (True, "ok", {"K1": "V0", "K2": "V3"}),
        (1, "ok", {"K1": "V0", "K2": "V3"}),
        ("one", "ok", {"K1": "V0", "K2": "V3"}),
        (False, "not_ok", {"K1": "V2"}),
        (0, "not_ok", {"K1": "V2"}),
        (None, "not_ok", {"K1": "V2"}),
        ([], "not_ok", {"K1": "V2"}),
    ],
)
@pytest.mark.asyncio
async def test_if_component_jump(condition: Any, label: str, jump_data: dict):
    bot = create_bot()
    thread = create_thread()
    flow = "flow"
    data = {"K1": "V2"}
    stack = []

    def jump(label: str):
        return to_spec(
            JumpComponent(jump=StepLabelRef(label), context_flow=FlowRef(flow))
        )

    component = IfComponent(
        if_=condition, then=jump("ok"), else_=jump("not_ok")
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
