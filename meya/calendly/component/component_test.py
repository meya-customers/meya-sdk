import pytest

from meya.button.spec import ButtonEventSpec
from meya.button.trigger import ButtonTrigger
from meya.calendly.component import CalendlyComponent
from meya.calendly.component import CalendlyComponentResponse
from meya.calendly.component import CalendlyState
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyWebhook
from meya.calendly.payload.payload_test import SAMPLED_INVITEE_CREATED
from meya.calendly.trigger import CalendlyTrigger
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import create_user
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.text.event.say import SayEvent
from meya.tile.event.ask import TileAskEvent
from meya.tile.spec import TileEventSpec
from meya.util.dict import to_dict
from meya.util.json import to_json
from typing import Optional


@pytest.mark.parametrize(
    ("calendly", "button_text", "prefill", "webhook_data"),
    [
        (
            "erik-meya/meya-demo",
            None,
            dict(name="Greta Thunberg", email="greta@meya.ai"),
            SAMPLED_INVITEE_CREATED,
        ),
        ("person1/calendar1", None, None, SAMPLED_INVITEE_CREATED),
        (
            "person2/calendar2",
            "Let's do it!",
            dict(foo="bar"),
            SAMPLED_INVITEE_CREATED,
        ),
    ],
)
@pytest.mark.asyncio
async def test_calendly_component(
    calendly: str,
    button_text: Optional[str],
    prefill: Optional[dict],
    webhook_data: dict,
):
    kwargs = dict(calendly=calendly, prefill=prefill)
    if button_text is not None:
        kwargs["button_text"] = button_text
    if prefill is not None:
        kwargs["prefill"] = prefill
    button_text = button_text or "Book a meeting"
    thread = create_thread()
    user = create_user()
    booking_id = "bk-~0"

    component = CalendlyComponent(**kwargs)
    component_start_entry = create_component_start_entry(
        component, thread=thread
    )

    # calendly tile
    popup_closed_button_id = "b-~1"
    event_scheduled_button_id = "b-~2"
    calendly_button = "b-~3"
    cancel_button = "b-~4"
    lifecycle_buttons = {
        "popupClosed": popup_closed_button_id,
        "eventScheduled": event_scheduled_button_id,
    }
    popup_options = dict(
        url=f"https://calendly.com/{calendly}",
        utm=dict(
            utmCampaign=None,
            utmSource="meya",
            utmMedium=None,
            utmContent=f"{thread.id}:{user.id}:{booking_id}",
            utmTerm=None,
        ),
    )
    if prefill:
        popup_options["prefill"] = prefill
    life_cycle_javascript = component.generate_lifecycle_javascript()
    ask_tiles = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                buttons=[
                    ButtonEventSpec(
                        text=button_text,
                        javascript=(
                            f"var lifecycleButtons = {to_json(lifecycle_buttons)};"
                            f"var popupOptions = {to_json(popup_options)};"
                            f"{life_cycle_javascript}"
                        ),
                        button_id=calendly_button,
                    ),
                    ButtonEventSpec(
                        text=component.cancel_text, button_id=cancel_button
                    ),
                ]
            )
        ],
    )

    def state_data(state: CalendlyState) -> dict:
        return {
            CalendlyComponent.BOOKING_ID_KEY: booking_id,
            CalendlyComponent.POPUP_CLOSED_BUTTON_ID_KEY: popup_closed_button_id,
            CalendlyComponent.EVENT_SCHEDULED_BUTTON_ID_KEY: event_scheduled_button_id,
            CalendlyComponent.STATE_KEY: state.value,
        }

    # cancel button
    cancel_next_entry = create_flow_next_entry(
        component_start_entry,
        data=to_dict(CalendlyComponentResponse(result=None)),
    )
    cancel_button_trigger_element = ButtonTrigger(
        action=create_trigger_action_entry(cancel_next_entry),
        button_id=cancel_button,
        text=component.cancel_text,
    )

    # popup_closed callback
    popup_closed_next_entry = create_component_next_entry(
        component_start_entry, data=state_data(CalendlyState.CLOSED)
    )
    popup_closed_trigger_element = ButtonTrigger(
        action=create_trigger_action_entry(popup_closed_next_entry),
        button_id=popup_closed_button_id,
        text="calendly.popup_closed",
    )

    # event_scheduled callback
    event_scheduled_next_entry = create_component_next_entry(
        component_start_entry, data=state_data(CalendlyState.PENDING)
    )
    event_scheduled_trigger_element = ButtonTrigger(
        action=create_trigger_action_entry(event_scheduled_next_entry),
        button_id=event_scheduled_button_id,
        text="calendly.event_scheduled",
    )

    # invitee.created action
    invitee_created_action_entry = create_component_next_entry(
        component_start_entry, data=state_data(CalendlyState.BOOKED)
    )
    # invitee.created trigger
    created_trigger_element = CalendlyTrigger(
        calendly_event=CalendlyEventType.INVITEE_CREATED.value,
        booking_id=booking_id,
        action=create_trigger_action_entry(invitee_created_action_entry),
    )

    # verify start()
    await verify_process_element(
        component,
        component_start_entry,
        [
            ask_tiles,
            *activate_triggers(
                component_start_entry,
                cancel_button_trigger_element,
                created_trigger_element,
                popup_closed_trigger_element,
                event_scheduled_trigger_element,
            ),
        ],
        user=user,
        thread=thread,
    )

    # verify next("closed")

    # try again button
    try_again_button = "b-~3"
    cancel_button = "b-~4"
    try_again_next_entry = create_component_next_entry(
        component_start_entry, data=state_data(CalendlyState.INITIAL)
    )
    try_again_button_trigger_element = ButtonTrigger(
        action=create_trigger_action_entry(try_again_next_entry),
        button_id=try_again_button,
        text=component.try_again_text,
    )

    cancel_next_entry = create_flow_next_entry(
        cancel_next_entry, data=state_data(CalendlyState.CLOSED)
    )
    cancel_trigger_element = ButtonTrigger(
        action=create_trigger_action_entry(cancel_next_entry),
        button_id=cancel_button,
        text=component.cancel_text,
    )
    say_event = SayEvent(
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        quick_replies=[
            ButtonEventSpec(
                text=component.try_again_text, button_id=try_again_button
            ),
            ButtonEventSpec(
                text=component.cancel_text, button_id=cancel_button
            ),
        ],
        text=component.closed_text,
    )
    await verify_process_element(
        component,
        popup_closed_next_entry,
        [
            say_event,
            *activate_triggers(
                component_start_entry,
                try_again_button_trigger_element,
                cancel_trigger_element,
                created_trigger_element,
            ),
        ],
        user=user,
        thread=thread,
    )

    # verify next("pending")
    say_event = SayEvent(
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        text=component.pending_text,
    )
    await verify_process_element(
        component,
        event_scheduled_next_entry,
        [
            say_event,
            *activate_triggers(
                event_scheduled_next_entry, created_trigger_element
            ),
        ],
        user=user,
        thread=thread,
    )

    # verify next("booked")
    webhook = CalendlyWebhook.from_dict(webhook_data)
    webhook.payload.tracking.utm_content = CalendlyWebhook.encode_utm_content(
        thread_id=thread.id, user_id=user.id, booking_id=booking_id
    )
    invitee_created_next_entry = create_component_next_entry(
        invitee_created_action_entry,
        data={
            CalendlyTrigger.EVENT_KEY: webhook.to_event().to_typed_dict(
                test_type_registry
            )
        },
    )
    flow_next_entry = create_flow_next_entry(
        invitee_created_next_entry,
        data=to_dict(
            CalendlyComponentResponse(result=webhook), preserve_nones=True
        ),
    )
    flow_next_entry.data.pop(CalendlyTrigger.EVENT_KEY)
    flow_next_entry.data.pop(CalendlyComponent.BOOKING_ID_KEY)
    flow_next_entry.data.pop(CalendlyComponent.POPUP_CLOSED_BUTTON_ID_KEY)
    flow_next_entry.data.pop(CalendlyComponent.EVENT_SCHEDULED_BUTTON_ID_KEY)
    flow_next_entry.data.pop(CalendlyComponent.STATE_KEY)
    await verify_process_element(
        component,
        invitee_created_next_entry,
        [flow_next_entry],
        user=user,
        thread=thread,
    )
