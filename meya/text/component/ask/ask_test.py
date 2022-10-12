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
from meya.text.component.ask import AskComponent
from meya.text.component.ask import ComposerElementSpec
from meya.text.event.ask import AskEvent
from meya.text.trigger.catchall import CatchallTrigger
from meya.util.dict import to_dict


@pytest.mark.asyncio
async def test_component_start():
    component = AskComponent(
        ask="What elephant?",
        quick_replies=["African Elephant", "Asian Elephant"],
        composer=ComposerElementSpec(placeholder="Question?"),
    )
    component_start_entry = create_component_start_entry(component)
    ask_event = AskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.TEXT,
            placeholder="Question?",
            visibility=ComposerVisibility.SHOW,
        ),
        quick_replies=[
            ButtonEventSpec(text="African Elephant"),
            ButtonEventSpec(text="Asian Elephant"),
        ],
        text="What elephant?",
    )
    triggers = activate_triggers(
        component_start_entry,
        CatchallTrigger(
            confidence=CatchallTrigger.MAX_CONFIDENCE,
            action=create_trigger_action_entry(
                create_component_next_entry(component_start_entry)
            ),
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_event, *triggers]
    )


@pytest.mark.asyncio
async def test_component_next():
    component = AskComponent(ask=None)
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={CatchallTrigger.RESULT_KEY: "Kawhi Leonard"},
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry,
        data=to_dict(ComponentOkResponse(result="Kawhi Leonard")),
    )
    await verify_process_element(
        component, component_next_entry, [flow_next_entry]
    )
