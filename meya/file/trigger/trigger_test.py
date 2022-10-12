import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.file.event import FileEvent
from meya.file.trigger import FileTrigger


@pytest.mark.asyncio
async def test_trigger():
    event = FileEvent(
        filename="cheatsheet.pdf",
        thread_id="t-0",
        url="https://upload.wikimedia.org/wikipedia/commons/b/b3/Wiki_markup_cheatsheet_EN.pdf",
        user_id="u-0",
    )
    trigger = FileTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        )
    )
    match_data = {FileTrigger.RESULT_KEY: event.url}
    await verify_trigger_match(
        trigger, event, should_match=True, match_data=match_data
    )
