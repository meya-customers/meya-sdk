from dataclasses import dataclass
from meya.calendly.event import CalendlyEvent
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyWebhook
from meya.element.field import element_field
from meya.element.field import process_field
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Optional


@dataclass
class CalendlyTrigger(Trigger):
    """
    This trigger will match on incoming Calendly webhook payloads when:'
    - calendly_event (ex. "invitee.created" matches)
    - all of optional conditions match
    - optional: booking_id, event_type_slug, assigned_to_email
    This trigger can be used in transition as part of CalendlyComponent
    or to start flows using slug and/or email conditions.
    The when condition can also be useful to inspect deeper payload conditions
    """

    calendly_event: str = element_field(signature=True)
    booking_id: Optional[str] = element_field(default=None)
    event_type_slug: Optional[str] = element_field(default=None)
    assigned_to_email: Optional[str] = element_field(default=None)

    entry: CalendlyEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        if (
            self.is_calendly_event_match
            and self.is_booking_id_match
            and self.is_event_type_slug_match
            and self.is_assigned_to_email_match
        ):
            return self.succeed()
        else:
            return self.fail()

    @property
    def is_calendly_event_match(self) -> bool:
        try:
            return self.webhook.event == CalendlyEventType(self.calendly_event)
        except ValueError:
            return False

    @property
    def is_booking_id_match(self) -> bool:
        if self.booking_id is None:
            return True
        return self.webhook.booking_id == self.booking_id

    @property
    def is_event_type_slug_match(self) -> bool:
        if self.event_type_slug is None:
            return True
        return self.webhook.payload.event_type.slug == self.event_type_slug

    @property
    def is_assigned_to_email_match(self) -> bool:
        if self.assigned_to_email is None:
            return True
        for assigned_to in self.webhook.payload.event.extended_assigned_to:
            if assigned_to.email == self.assigned_to_email:
                return True
        return False

    @property
    def webhook(self) -> CalendlyWebhook:
        return CalendlyWebhook.from_dict(self.entry.data)
