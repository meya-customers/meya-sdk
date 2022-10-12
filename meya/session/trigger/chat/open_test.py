import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.session.event.chat.open import ChatOpenEvent
from meya.session.trigger.chat.open import ChatOpenTrigger


@pytest.mark.asyncio
async def test_trigger():
    event = ChatOpenEvent(thread_id="t-0", user_id="u-0")
    trigger = ChatOpenTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        )
    )
    match_data = {}
    await verify_trigger_match(
        trigger, event, should_match=True, match_data=match_data
    )
