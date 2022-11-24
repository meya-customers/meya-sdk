import pytest

from meya.button.trigger import ButtonTrigger
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import to_spec
from meya.element.element_test import verify_process_element
from meya.flow.component.jump import JumpComponent
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.whatsapp.component.list_picker import ListPickerComponent
from meya.whatsapp.component.spec import ListPickerItemElementSpec
from meya.whatsapp.event.list_picker import ListPickerEvent
from meya.whatsapp.event.list_picker import ListPickerItemEventSpec


@pytest.mark.asyncio
async def test_list_picker():
    bot = create_bot()
    thread = create_thread()
    component = ListPickerComponent(
        list_picker="Choose an option",
        button="Select",
        items=[
            ListPickerItemElementSpec(
                text="Button 1",
                description="Button 1 description",
                result={"k": "1"},
            ),
            ListPickerItemElementSpec(
                text="Button 2",
                description="Button 2 description",
                result=2,
            ),
            ListPickerItemElementSpec(
                text="Button 5",
                description="Button 5 description",
                action=to_spec(
                    JumpComponent(
                        jump=StepLabelRef("j5"), context_flow=FlowRef("test")
                    )
                ),
            ),
        ],
    )
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread
    )
    list_picker_event = ListPickerEvent(
        body="Choose an option",
        button="Select",
        items=[
            ListPickerItemEventSpec(
                text="Button 1",
                description="Button 1 description",
                button_id="b-~0",
            ),
            ListPickerItemEventSpec(
                text="Button 2",
                description="Button 2 description",
                button_id="b-~1",
            ),
            ListPickerItemEventSpec(
                text="Button 5",
                description="Button 5 description",
                button_id="b-~2",
            ),
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result={"k": "1"})
                )
            ),
            button_id="b-~0",
            text="Button 1",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=2)
                )
            ),
            button_id="b-~1",
            text="Button 2",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_component_start_entry(
                    JumpComponent(
                        jump=StepLabelRef("j5"), context_flow=FlowRef("test")
                    ),
                    bot=bot,
                    thread=thread,
                    flow=component_start_entry.flow,
                )
            ),
            button_id="b-~2",
            text="Button 5",
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        [list_picker_event, *triggers],
        thread=thread,
        extra_elements=[bot],
    )
