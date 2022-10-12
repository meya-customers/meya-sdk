import pytest

from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_process_element
from meya.email.component.address.ask import EmailAddressAskComponent
from meya.email.trigger.address.address import EmailAddressTrigger
from meya.email.trigger.address.address import EmailAddressTriggerResponse
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.text.event.ask import AskEvent
from meya.util.dict import to_dict


@pytest.mark.parametrize(
    ("user_text", "user_email"),
    [
        ("test@meya.ai", "test@meya.ai"),
        ("Foo@Bar.ai", "Foo@bar.ai"),
        ("Foo@Почта.рф", "Foo@почта.рф"),
        ("Foo@xn--80a1acny.xn--p1ai", "Foo@почта.рф"),
        ("Фью@Bar.com", "Фью@bar.com"),
    ],
)
@pytest.mark.asyncio
async def test_component_next_valid(user_text: str, user_email: str):
    component = EmailAddressAskComponent(ask="What is your email?")
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data=to_dict(EmailAddressTriggerResponse(result=user_email)),
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry,
        data=to_dict(ComponentOkResponse(result=user_email)),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[flow_next_entry],
    )


@pytest.mark.parametrize(
    ("user_text",),
    [("bogus",), ("@bogus.com",), ("bogus@.com",), ("bogus@gmail.con",)],
)
@pytest.mark.asyncio
async def test_component_next_invalid_retry(user_text: str):
    component = EmailAddressAskComponent(
        ask="What is your email?",
        error_message="Invalid email, please try again.",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data=to_dict(EmailAddressTriggerResponse(result="")),
    )
    ask_event = AskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.TEXT, visibility=ComposerVisibility.SHOW
        ),
        text=component.error_message,
    )
    triggers = activate_triggers(
        component_next_entry,
        EmailAddressTrigger(
            confidence=component.confidence,
            action=create_trigger_action_entry(
                create_component_next_entry(
                    component_next_entry,
                    data=to_dict(
                        ComponentErrorResponse(result="", retry_count=1)
                    ),
                )
            ),
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[ask_event, *triggers],
    )


@pytest.mark.parametrize(
    ("user_text",),
    [("bogus",), ("@bogus.com",), ("bogus@.com",), ("bogus@gmail.con",)],
)
@pytest.mark.asyncio
async def test_invalid_email_no_catchall(user_text: str):
    component = EmailAddressAskComponent(ask="What is your email?", retries=1)
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            **to_dict(EmailAddressTriggerResponse(result="")),
            **to_dict(ComponentErrorResponse(result="", retry_count=1)),
        },
    )
    flow_next_entry = create_flow_next_entry(component_next_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[flow_next_entry],
    )
