import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.element.element_test import create_bot
from meya.element.element_test import create_thread
from meya.element.element_test import to_spec
from meya.element.element_test import to_spec_dict
from meya.element.element_test import verify_process_element
from meya.flow.component.jump import JumpComponent
from meya.flow.component.match import MatchComponent
from meya.flow.component.match import MatchComponentResponse
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.util.dict import to_dict
from typing import Any


@pytest.mark.parametrize(
    ("value", "label", "response"),
    [
        ("a", "l0", MatchComponentResponse(result="a", groups={}, ok=True)),
        (
            "aaaa",
            "l1",
            MatchComponentResponse(result="aaaa", groups={}, ok=True),
        ),
        (
            "qaaay",
            "l1",
            MatchComponentResponse(result="aaa", groups={}, ok=True),
        ),
        (
            "bb",
            "l2",
            MatchComponentResponse(
                result="b", groups={0: "b", "b_group": "b"}, ok=True
            ),
        ),
        ("c", "l3", MatchComponentResponse(result="c", groups={}, ok=False)),
        ("d", "l3", MatchComponentResponse(result="d", groups={}, ok=False)),
        (9, "l3", MatchComponentResponse(result=9, groups={}, ok=False)),
    ],
)
@pytest.mark.asyncio
async def test_match_component_jump(
    value: Any, label: str, response: MatchComponentResponse
):
    bot = create_bot()
    thread = create_thread()

    flow = "flow"
    data = {"K1": "V2"}
    stack = []

    def jump(label: str):
        return to_spec(
            JumpComponent(jump=StepLabelRef(label), context_flow=FlowRef(flow))
        )

    component = MatchComponent(
        value=value,
        match={
            "a": jump("l0"),
            "A+": jump("l1"),
            "(?P<b_group>a | b)\n": jump("l2"),
            "e": jump("l4"),
        },
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
        data={**data, **to_dict(response)},
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
