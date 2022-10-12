import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_say_event
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.text.trigger.catchall import CatchallTrigger


@pytest.mark.parametrize(
    ("text", "confidence"),
    [("hi", None), ("random", None), ("hi", 1.0), ("hello", 1)],
)
@pytest.mark.asyncio
async def test_trigger(text: str, confidence: float):
    event = create_say_event(text)
    trigger = CatchallTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        ),
        confidence=confidence,
    )
    match_data = {CatchallTrigger.RESULT_KEY: text}
    await verify_trigger_match(
        trigger,
        event,
        should_match=True,
        confidence=confidence,
        original_confidence=CatchallTrigger.MIN_CONFIDENCE,
        match_data=match_data,
    )
