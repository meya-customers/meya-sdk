import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.session.event.page.open import PageOpenEvent
from meya.session.trigger.page.open import PageOpenTrigger
from typing import Optional


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("trigger_magic_link_error", "event_magic_link_ok", "should_match"),
    [
        (None, None, True),
        (None, True, True),
        (None, False, True),
        (True, None, False),
        (True, True, False),
        (True, False, True),
        (False, None, True),
        (False, True, True),
        (False, False, False),
    ],
)
async def test_trigger(
    trigger_magic_link_error: Optional[bool],
    event_magic_link_ok: Optional[bool],
    should_match: bool,
):
    event = PageOpenEvent(
        magic_link_ok=event_magic_link_ok,
        thread_id="t-0",
        url="https://meya.ai",
        user_id="u-0",
        context={},
    )
    trigger = PageOpenTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
        magic_link_error=trigger_magic_link_error,
    )
    match_data = dict(result=event.url, context={})
    await verify_trigger_match(
        trigger, event, should_match=should_match, match_data=match_data
    )
