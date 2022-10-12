import pytest

from meya.button.spec import ButtonEventSpec
from meya.component.element import ComponentOkResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import create_user
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconEventSpec
from meya.text.component.ask.form import AskFormComponent
from meya.text.component.ask.form import ComposerElementSpec
from meya.util.dict import to_dict


@pytest.mark.asyncio
async def test_component_start():
    component = AskFormComponent(
        ask_form="Name?",
        quick_replies=["No name"],
        composer=ComposerElementSpec(visibility=ComposerVisibility.HIDE),
        autocomplete="name",
        placeholder="Name here",
        icon="streamline-regular/17-users/04-geometric-full body-single user-woman/single-woman-question.svg",
        field_name="uname",
        label="Name",
    )
    component_start_entry = create_component_start_entry(component)
    form_event = FormAskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.BLUR, visibility=ComposerVisibility.HIDE
        ),
        form_id="form-~0",
        fields=[
            Field(
                name="uname",
                autocomplete="name",
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/17-users/04-geometric-full-body-single-user-woman/single-woman-question.svg"
                ),
                placeholder="Name here",
                label="Name",
                required=True,
                type=FieldType.TEXT,
            )
        ],
        quick_replies=[ButtonEventSpec(text="No name")],
        text="Name?",
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


@pytest.mark.asyncio
async def test_component_next():
    component = AskFormComponent(ask_form="Name?")
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"text": "X"},
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
        component_next_entry, data=to_dict(ComponentOkResponse(result="X"))
    )
    form_ok_event = FormOkEvent(form_id="form_1")
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_ok_event, flow_next_entry],
    )
