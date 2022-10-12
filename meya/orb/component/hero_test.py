import pytest

from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.button.trigger import ButtonTrigger
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import to_spec
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerEventSpec
from meya.flow.component import FlowComponent
from meya.flow.element import FlowRef
from meya.orb.component.hero import HeroComponent
from meya.orb.event.hero import HeroEvent


@pytest.mark.asyncio
async def test_hero_component():
    bot = create_bot()
    thread = create_thread()
    component = HeroComponent(
        hero="Welcome!",
        description="How can I help?",
        quick_replies=[
            "Sales",
            ButtonElementSpec(
                text="Support",
                action=to_spec(FlowComponent(flow=FlowRef("support"))),
            ),
        ],
        composer=ComposerElementSpec(placeholder="Anything else?"),
    )
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread
    )
    text_event = HeroEvent(
        composer=ComposerEventSpec(placeholder="Anything else?"),
        description="How can I help?",
        quick_replies=[
            ButtonEventSpec(text="Sales"),
            ButtonEventSpec(text="Support", button_id="b-~0"),
        ],
        title="Welcome!",
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_component_start_entry(
                    FlowComponent(flow=FlowRef("support")),
                    bot=bot,
                    thread=thread,
                    flow=component_start_entry.flow,
                )
            ),
            button_id="b-~0",
            text="Support",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[text_event, *triggers],
        thread=thread,
        extra_elements=[bot],
    )
