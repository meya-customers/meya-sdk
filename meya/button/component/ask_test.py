import pytest

from meya.button.component.ask import ButtonAskComponent
from meya.button.component.ask import ComposerElementSpec
from meya.button.event.ask import ButtonAskEvent
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.button.trigger import ButtonTrigger
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import to_spec
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.flow.component import FlowComponent
from meya.flow.component.jump import JumpComponent
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconEventSpec


@pytest.mark.asyncio
async def test_action_buttons():
    bot = create_bot()
    thread = create_thread()
    component = ButtonAskComponent(
        ask="Choose a button",
        buttons=[
            ButtonElementSpec(text="Button 1", result={"k": "1"}),
            ButtonElementSpec(text="Button 2", result=2),
            ButtonElementSpec(
                text="Button 5",
                action=to_spec(
                    JumpComponent(
                        jump=StepLabelRef("j5"), context_flow=FlowRef("test")
                    )
                ),
            ),
        ],
        quick_replies=[
            ButtonElementSpec(text="Text 3", result=None),
            ButtonElementSpec(
                text="Text 4",
                action=to_spec(FlowComponent(flow=FlowRef("f4"))),
            ),
        ],
        composer=ComposerElementSpec(visibility=ComposerVisibility.HIDE),
    )
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread
    )
    ask_buttons_event = ButtonAskEvent(
        buttons=[
            ButtonEventSpec(text="Button 1", button_id="b-~0"),
            ButtonEventSpec(text="Button 2", button_id="b-~1"),
            ButtonEventSpec(text="Button 5", button_id="b-~2"),
        ],
        composer=ComposerEventSpec(
            focus=ComposerFocus.BLUR, visibility=ComposerVisibility.HIDE
        ),
        quick_replies=[
            ButtonEventSpec(text="Text 3", button_id="b-~3"),
            ButtonEventSpec(text="Text 4", button_id="b-~4"),
        ],
        text="Choose a button",
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
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=None)
                )
            ),
            button_id="b-~3",
            text="Text 3",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_component_start_entry(
                    FlowComponent(flow=FlowRef("f4")),
                    bot=bot,
                    thread=thread,
                    flow=component_start_entry.flow,
                )
            ),
            button_id="b-~4",
            text="Text 4",
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        [ask_buttons_event, *triggers],
        thread=thread,
        extra_elements=[bot],
    )


@pytest.mark.asyncio
async def test_action_quick_reply():
    component = ButtonAskComponent(
        ask=None,
        buttons=[ButtonElementSpec(text="Button 1")],
        quick_replies=[ButtonElementSpec(text="Button 2", result=2)],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[ButtonEventSpec(text="Button 1")],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[ButtonEventSpec(text="Button 2", button_id="b-~0")],
        text=None,
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=2)
                )
            ),
            button_id="b-~0",
            text="Button 2",
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, *triggers]
    )


@pytest.mark.asyncio
async def test_magic_buttons():
    component = ButtonAskComponent(
        buttons=[
            ButtonElementSpec(text="Button 1", result=1),
            ButtonElementSpec(text="Button 2", result=2, magic=True),
        ],
        quick_replies=[ButtonElementSpec(result=3)],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[ButtonEventSpec(text="Button 1", button_id="b-~0")],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        text=None,
        thread_id=component_start_entry.thread_id,
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=1)
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
                create_flow_next_entry(
                    component_start_entry, data=dict(result=3)
                )
            ),
            button_id="b-~2",
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, *triggers]
    )


@pytest.mark.asyncio
async def test_text_buttons():
    component = ButtonAskComponent(
        buttons=["Button 2", ButtonElementSpec(text="Button 3")],
        quick_replies=[ButtonElementSpec(text="Text 1"), "Text 2"],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[
            ButtonEventSpec(text="Button 2"),
            ButtonEventSpec(text="Button 3"),
        ],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[
            ButtonEventSpec(text="Text 1"),
            ButtonEventSpec(text="Text 2"),
        ],
        text=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_javascript_buttons():
    component = ButtonAskComponent(
        buttons=[
            ButtonElementSpec(text="Button 3", javascript="alert('b-3')")
        ],
        quick_replies=[
            ButtonElementSpec(text="Text 1", javascript="alert('t-1')")
        ],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[
            ButtonEventSpec(
                text="Button 3", javascript="alert('b-3')", button_id="b-~0"
            )
        ],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[
            ButtonEventSpec(
                text="Text 1", javascript="alert('t-1')", button_id="b-~1"
            )
        ],
        text=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_static_buttons():
    component = ButtonAskComponent(
        buttons=[
            ButtonElementSpec(
                text="Button 3", button_id="b-3", context=dict(auth=True)
            )
        ],
        quick_replies=[ButtonElementSpec(text="Text 1", button_id="t-1")],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[
            ButtonEventSpec(
                text="Button 3", button_id="b-3", context=dict(auth=True)
            )
        ],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[ButtonEventSpec(text="Text 1", button_id="t-1")],
        text=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_link_buttons():
    component = ButtonAskComponent(
        buttons=[ButtonElementSpec(text="Button 4", url="http://example.org")],
        quick_replies=[
            ButtonElementSpec(text="Text 1", url="http://example.org?quick")
        ],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[ButtonEventSpec(text="Button 4", url="http://example.org")],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[
            ButtonEventSpec(text="Text 1", url="http://example.org?quick")
        ],
        text=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_button_icons():
    component = ButtonAskComponent(
        buttons=[
            ButtonElementSpec(
                icon="streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg"
            ),
            ButtonElementSpec(
                text="Button 1",
                icon=IconElementSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                ),
            ),
        ],
        quick_replies=[
            ButtonElementSpec(
                icon=IconElementSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                )
            ),
            ButtonElementSpec(
                text="Text 2",
                icon="streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg",
            ),
        ],
    )
    component_start_entry = create_component_start_entry(component)
    ask_buttons_event = ButtonAskEvent(
        buttons=[
            ButtonEventSpec(
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg"
                )
            ),
            ButtonEventSpec(
                text="Button 1",
                icon=IconEventSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                ),
            ),
        ],
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[
            ButtonEventSpec(
                icon=IconEventSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                )
            ),
            ButtonEventSpec(
                text="Text 2",
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg"
                ),
            ),
        ],
        text=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_buttons_event, flow_next_entry]
    )
