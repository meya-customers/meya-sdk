import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_say_event
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.text.trigger.keyword import KeywordTrigger
from typing import Optional


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "keyword", "ignorecase", "should_match"),
    [
        ("hi", "hi", None, True),
        ("hI", "Hi", None, True),
        ("hi", "hi", True, True),
        ("hI", "Hi", True, True),
        ("hi", "hi", False, True),
        ("hI", "Hi", False, False),
        ("a", "b", None, False),
        ("a", "b", True, False),
        ("a", "b", False, False),
        (None, "b", True, None),
    ],
)
async def test_keyword_trigger(
    text: Optional[str],
    keyword: str,
    ignorecase: Optional[bool],
    should_match: Optional[bool],
):
    event = create_say_event(text=text)
    trigger = KeywordTrigger(
        keyword=keyword,
        ignorecase=ignorecase,
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
    )
    match_data = {trigger.RESULT_KEY: event.text}
    await verify_trigger_match(
        trigger, event, should_match=should_match, match_data=match_data
    )
