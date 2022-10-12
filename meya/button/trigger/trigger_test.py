import pytest

from meya.button.event.click import ButtonClickEvent
from meya.button.trigger import ButtonTrigger
from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("trigger_button_id", "event_button_id", "event_context", "should_match"),
    [
        ("b-1", "b-1", {}, True),
        ("b-1", "b-1", dict(x="y"), True),
        ("b-1", "b-2", {}, False),
        ("b-1", "b-1", {}, True),
        ("b-1", "b-1", dict(x="y"), True),
        ("b-1", "b-2", {}, False),
    ],
)
async def test_trigger(
    trigger_button_id: str,
    event_button_id: str,
    event_context: dict,
    should_match: bool,
):
    event = ButtonClickEvent(
        button_id=event_button_id,
        context=event_context,
        text="x",
        thread_id="t-0",
        user_id="u-0",
    )
    trigger = ButtonTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
        button_id=trigger_button_id,
    )
    match_data = dict(context=event_context or {})
    await verify_trigger_match(
        trigger,
        event,
        should_match=should_match,
        match_data=match_data,
        expected_db_requests=[],
    )
