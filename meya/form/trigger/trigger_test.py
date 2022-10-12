import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger


@pytest.mark.asyncio
async def test_trigger():
    event = FormSubmitEvent(
        form_id="form_1",
        fields={"email": "test@meya.ai"},
        thread_id="t-0",
        user_id="u-0",
    )
    trigger = FormTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        ),
        form_id=event.form_id,
    )
    match_data = {FormTrigger.RESULT_KEY: {"email": "test@meya.ai"}}
    await verify_trigger_match(
        trigger, event, should_match=True, match_data=match_data
    )
