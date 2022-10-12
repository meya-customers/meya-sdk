import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_say_event
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.email.trigger.address.address import EmailAddressTrigger
from meya.email.trigger.address.address import EmailAddressTriggerResponse
from meya.util.dict import to_dict


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "confidence", "should_match", "result"),
    [
        ("test@test.com", None, True, "test@test.com"),
        ("Foo@Bar.ai", None, True, "Foo@bar.ai"),
        ("Foo@Почта.рф", None, True, "Foo@почта.рф"),
        ("Foo@xn--80a1acny.xn--p1ai", None, True, "Foo@почта.рф"),
        ("Фью@Bar.com", None, True, "Фью@bar.com"),
        ("test", None, False, ""),
        ("test", EmailAddressTrigger.MAX_CONFIDENCE, True, ""),
        ("Foo@Bar.ai", EmailAddressTrigger.MAX_CONFIDENCE, True, "Foo@bar.ai"),
        (
            "Foo@Почта.рф",
            EmailAddressTrigger.MAX_CONFIDENCE,
            True,
            "Foo@почта.рф",
        ),
        (
            "Foo@xn--80a1acny.xn--p1ai",
            EmailAddressTrigger.MAX_CONFIDENCE,
            True,
            "Foo@почта.рф",
        ),
        (
            "Фью@Bar.com",
            EmailAddressTrigger.MAX_CONFIDENCE,
            True,
            "Фью@bar.com",
        ),
    ],
)
async def test_trigger(text, confidence, should_match, result):
    event = create_say_event(text)
    trigger = EmailAddressTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
        confidence=confidence,
    )
    match_data = to_dict(EmailAddressTriggerResponse(result=result))
    await verify_trigger_match(
        trigger,
        event,
        should_match=should_match,
        confidence=confidence,
        match_data=match_data,
    )
