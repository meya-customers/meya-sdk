import pytest

from meya.button.spec import ButtonEventSpec
from meya.component.element import ComponentOkResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.file.component.ask import ComposerElementSpec
from meya.file.component.ask import FileAskComponent
from meya.file.trigger import FileTrigger
from meya.text.event.ask import AskEvent
from meya.util.dict import to_dict


@pytest.mark.asyncio
async def test_component_start():
    component = FileAskComponent(
        ask="Upload your invoice",
        quick_replies=["Exit"],
        composer=ComposerElementSpec(placeholder="Invoice"),
    )
    component_start_entry = create_component_start_entry(component)
    ask_event = AskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.FILE,
            placeholder="Invoice",
            visibility=ComposerVisibility.SHOW,
        ),
        quick_replies=[ButtonEventSpec(text="Exit")],
        text="Upload your invoice",
    )
    triggers = activate_triggers(
        component_start_entry,
        FileTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(component_start_entry)
            )
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_event, *triggers]
    )


@pytest.mark.asyncio
async def test_component_next():
    component = FileAskComponent(ask="Which file?")
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={FileTrigger.RESULT_KEY: "file.pdf"},
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry,
        data=to_dict(ComponentOkResponse(result="file.pdf")),
    )
    await verify_process_element(
        component, component_next_entry, [flow_next_entry]
    )
