import pytest

from meya.button.event.click import ButtonClickEvent
from meya.component.entry.start import ComponentStartEntry
from meya.core.type_registry import TypeRegistry
from meya.element.element_error import ElementValidationError
from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_trigger_match
from meya.event.entry import Event
from meya.event.trigger.type import TypeTrigger
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent
from typing import Optional


@pytest.mark.parametrize(
    ("event_type", "validation_message"),
    [
        (SayEvent.get_entry_type(test_type_registry), None),
        (
            SayComponent.get_element_type(test_type_registry),
            'invalid event type "meya.text.component.say"',
        ),
        (
            ComponentStartEntry.get_entry_type(test_type_registry),
            'invalid event type "meya.component.entry.start"',
        ),
        ("foo", 'invalid event type "foo"'),
    ],
)
def test_validate_type(event_type: str, validation_message: Optional[str]):
    trigger = TypeTrigger(
        event_type=event_type,
        action=create_trigger_action_entry(create_flow_start_entry()),
    )
    with TypeRegistry.current.set(test_type_registry):
        if validation_message:
            with pytest.raises(ElementValidationError) as excinfo:
                trigger.validate()
            assert str(excinfo.value) == validation_message
        else:
            trigger.validate()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("event_type", "event", "should_match"),
    [
        (
            SayEvent.get_entry_type(test_type_registry),
            SayEvent(
                user_id="u-123", text="t1", thread_id="t-0", trace_id="-"
            ),
            True,
        ),
        (
            SayEvent.get_entry_type(test_type_registry),
            ButtonClickEvent(
                button_id="b-1",
                text="Button",
                thread_id="t-0",
                user_id="u-123",
                trace_id="-",
            ),
            False,
        ),
        (
            ButtonClickEvent.get_entry_type(test_type_registry),
            SayEvent(
                user_id="u-123", text="t1", thread_id="t-0", trace_id="-"
            ),
            False,
        ),
        (
            ButtonClickEvent.get_entry_type(test_type_registry),
            ButtonClickEvent(
                button_id="b-1",
                text="Button",
                thread_id="t-0",
                user_id="u-123",
                trace_id="-",
            ),
            True,
        ),
    ],
)
async def test_type_trigger(event_type: str, event: Event, should_match: bool):
    trigger = TypeTrigger(
        event_type=event_type,
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
    )
    match_data = {
        TypeTrigger.EVENT_KEY: event.to_typed_dict(test_type_registry)
    }
    await verify_trigger_match(
        trigger, event, should_match=should_match, match_data=match_data
    )
