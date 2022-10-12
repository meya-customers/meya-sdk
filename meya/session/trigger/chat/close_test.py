import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.session.event.chat.close import ChatCloseEvent
from meya.session.trigger.chat.close import ChatCloseTrigger


@pytest.mark.asyncio
async def test_trigger():
    event = ChatCloseEvent(thread_id="t-0", user_id="u-0")
    trigger = ChatCloseTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        )
    )
    match_data = {}
    await verify_trigger_match(
        trigger, event, should_match=True, match_data=match_data
    )
