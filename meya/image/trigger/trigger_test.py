import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.image.event import ImageEvent
from meya.image.trigger import ImageTrigger


@pytest.mark.asyncio
async def test_trigger():
    event = ImageEvent(
        thread_id="t-0",
        url="https://66.media.tumblr.com/622e93c114159b9444e3fed8dd3e7636/tumblr_n5yye2rxBi1s5ibd1o1_1280.png",
        user_id="u-0",
    )
    trigger = ImageTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        )
    )
    match_data = {ImageTrigger.RESULT_KEY: event.url}
    await verify_trigger_match(
        trigger, event, should_match=True, match_data=match_data
    )
