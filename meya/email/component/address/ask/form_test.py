import pytest

from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.button.trigger import ButtonTrigger
from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import create_user
from meya.element.element_test import test_type_registry
from meya.element.element_test import to_spec
from meya.element.element_test import verify_process_element
from meya.email.component.address.ask.form import ComposerElementSpec
from meya.email.component.address.ask.form import EmailAddressAskFormComponent
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.flow.component import FlowComponent
from meya.flow.element import FlowRef
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.error import FormErrorEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconEventSpec
from meya.util.dict import to_dict


@pytest.mark.asyncio
async def test_component_start():
    component = EmailAddressAskFormComponent(
        ask_form="What is your email?",
        quick_replies=["Why email?"],
        composer=ComposerElementSpec(placeholder="Something else?"),
        error_message="Invalid email, please try again.",
        autocomplete="business_email",
        placeholder="Email here",
        field_name="work_email",
        label="Work email",
        icon="streamline-regular/19-emails/01-send-email/send-email-fly.svg",
    )
    component_start_entry = create_component_start_entry(component)
    form_event = FormAskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.BLUR, placeholder="Something else?"
        ),
        fields=[
            Field(
                name="work_email",
                autocomplete="business_email",
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/19-emails/01-send-email/send-email-fly.svg"
                ),
                placeholder="Email here",
                label="Work email",
                required=True,
                type=FieldType.EMAIL,
            )
        ],
        form_id="form-~0",
        quick_replies=[ButtonEventSpec(text="Why email?")],
        text="What is your email?",
    )
    triggers = activate_triggers(
        component_start_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(component_start_entry)
            ),
            form_id="form-~0",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[form_event, *triggers],
    )


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
    component = EmailAddressAskFormComponent(
        ask_form="What is your email?",
        error_message="Invalid email, please try again.",
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"email": user_text},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry,
        data=to_dict(ComponentOkResponse(result=user_email)),
    )
    form_ok_event = FormOkEvent(form_id="form_1")
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_ok_event, flow_next_entry],
    )


@pytest.mark.parametrize(
    ("user_text",),
    [("bogus",), ("@bogus.com",), ("bogus@.com",), ("bogus@gmail.con",)],
)
@pytest.mark.asyncio
async def test_component_next_invalid_retry(user_text: str):
    bot = create_bot()
    thread = create_thread()
    component = EmailAddressAskFormComponent(
        ask_form="What is your email?",
        error_message="Invalid email, please try again.",
        quick_replies=[
            ButtonElementSpec(
                text="Why email?",
                action=to_spec(FlowComponent(flow=FlowRef("f4"))),
            )
        ],
        composer=ComposerElementSpec(
            placeholder="EMAIL", visibility=ComposerVisibility.COLLAPSE
        ),
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"email": user_text},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component, bot=bot, thread=thread),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    form_error_event = FormErrorEvent(
        composer=ComposerEventSpec(
            placeholder="EMAIL", visibility=ComposerVisibility.COLLAPSE
        ),
        fields={"email": "Invalid email, please try again."},
        form_id="form_1",
        quick_replies=[ButtonEventSpec(text="Why email?", button_id="b-~0")],
    )
    triggers = activate_triggers(
        component_next_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(
                    component_next_entry,
                    data=to_dict(
                        ComponentErrorResponse(result=user_text, retry_count=1)
                    ),
                )
            ),
            form_id="form_1",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_component_start_entry(
                    FlowComponent(flow=FlowRef("f4")),
                    bot=bot,
                    thread=thread,
                    flow=component_next_entry.flow,
                    data=component_next_entry.data,
                )
            ),
            button_id="b-~0",
            text="Why email?",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_error_event, *triggers],
        thread=thread,
        extra_elements=[bot],
    )
