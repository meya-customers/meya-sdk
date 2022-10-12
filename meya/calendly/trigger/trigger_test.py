import pytest

from meya.calendly.payload.payload import CalendlyWebhook
from meya.calendly.payload.payload_test import INVITEE_CANCELED_PAYLOAD
from meya.calendly.payload.payload_test import INVITEE_CREATED_PAYLOAD
from meya.calendly.trigger import CalendlyTrigger
from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.event.entry import Event
from typing import Optional

INVITEE_CREATED_EVENT = CalendlyWebhook.from_dict(
    INVITEE_CREATED_PAYLOAD
).to_event()
INVITEE_CANCELED_EVENT = CalendlyWebhook.from_dict(
    INVITEE_CANCELED_PAYLOAD
).to_event()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "event",
        "calendly_event",
        "booking_id",
        "event_type_slug",
        "assigned_to_email",
        "should_match",
    ),
    [
        (INVITEE_CREATED_EVENT, "invitee.created", None, None, None, True),
        (INVITEE_CANCELED_EVENT, "invitee.canceled", None, None, None, True),
        (INVITEE_CANCELED_EVENT, "invitee.created", None, None, None, False),
        (
            INVITEE_CREATED_EVENT,
            "unsupported_event_type",
            None,
            None,
            None,
            False,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            "booking_id_here",
            None,
            None,
            True,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            "different_booking_id",
            None,
            None,
            False,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            None,
            "event_type_name",
            None,
            True,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            None,
            "different_event_type_slug",
            None,
            False,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            None,
            None,
            "user@example.com",
            True,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            None,
            None,
            "different_assigned_to_email",
            False,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            "booking_id_here",
            "event_type_name",
            "user@example.com",
            True,
        ),
        (
            INVITEE_CREATED_EVENT,
            "invitee.created",
            "booking_id_here",
            "different_event_type_slug",
            "user@example.com",
            False,
        ),
    ],
)
async def test_calendly_trigger(
    event: Event,
    calendly_event: str,
    booking_id: Optional[str],
    event_type_slug: Optional[str],
    assigned_to_email: Optional[str],
    should_match: bool,
):
    trigger = CalendlyTrigger(
        calendly_event=calendly_event,
        booking_id=booking_id,
        event_type_slug=event_type_slug,
        assigned_to_email=assigned_to_email,
        action=create_trigger_action_entry(
            create_flow_start_entry(thread_id=event.thread_id)
        ),
    )
    await verify_trigger_match(trigger, event, should_match=should_match)
