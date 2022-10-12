"""Calendly Webhook Event Models

These classes were initially generated using quicktype using
Calendly-provided example webhook json payloads. The dataclasses were then
modified manually.

- https://app.quicktype.io/ - Python 3.7, Classes only
- https://developer.calendly.com/docs/sample-webhook-data

"""

from dataclasses import dataclass
from datetime import datetime
from meya.calendly.event import CalendlyEvent
from meya.calendly.event.invitee.cancelled import CalendlyInviteeCancelledEvent
from meya.calendly.event.invitee.created import CalendlyInviteeCreatedEvent
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


class CalendlyEventType(SimpleEnum):
    INVITEE_CREATED = "invitee.created"
    INVITEE_CANCELED = "invitee.canceled"

    @classmethod
    def all(cls) -> List["CalendlyEventType"]:
        return [cls.INVITEE_CREATED, cls.INVITEE_CANCELED]


@dataclass
class ExtendedAssignedTo:
    name: str
    email: str
    primary: bool


@dataclass
class Event:
    uuid: str
    assigned_to: List[str]
    extended_assigned_to: List[ExtendedAssignedTo]
    start_time: datetime
    start_time_pretty: str
    invitee_start_time: datetime
    invitee_start_time_pretty: str
    end_time: datetime
    end_time_pretty: str
    invitee_end_time: datetime
    invitee_end_time_pretty: str
    created_at: datetime
    location: Optional[str]
    canceled: bool
    canceler_name: Optional[str]
    cancel_reason: Optional[str]
    canceled_at: Optional[datetime]


@dataclass
class Owner:
    type: str
    uuid: str


@dataclass
class EventType:
    uuid: str
    kind: str
    slug: str
    name: str
    duration: int
    owner: Owner


@dataclass
class Payment:
    id: str
    provider: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    terms: Optional[str]
    successful: Optional[bool]


@dataclass
class Invitee:
    uuid: str
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    email: str
    text_reminder_number: Optional[str]
    timezone: Optional[str]
    created_at: datetime
    is_reschedule: bool
    payments: List[Payment]
    canceled: bool
    canceler_name: Optional[str]
    cancel_reason: Optional[str]
    canceled_at: Optional[datetime]


@dataclass
class Tracking:
    utm_campaign: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_content: Optional[str]
    utm_term: Optional[str]
    salesforce_uuid: Optional[str]


@dataclass
class Payload:
    event_type: EventType
    event: Event
    invitee: Invitee
    questions_and_answers: list
    questions_and_responses: dict
    tracking: Tracking
    old_event: Any
    old_invitee: Any
    new_event: Any
    new_invitee: Any


@dataclass
class CalendlyWebhook:
    event: CalendlyEventType
    time: datetime
    payload: Payload

    def to_event(self) -> Optional[CalendlyEvent]:
        if (
            not (self.is_invitee_created or self.is_invitee_canceled)
            or self.thread_id is None
            or self.user_id is None
        ):
            return None
        klass = {
            CalendlyEventType.INVITEE_CREATED: CalendlyInviteeCreatedEvent,
            CalendlyEventType.INVITEE_CANCELED: CalendlyInviteeCancelledEvent,
        }[self.event]
        return klass(
            user_id=self.user_id,
            thread_id=self.thread_id,
            booking_id=self.booking_id,
            data=to_dict(self, preserve_nones=True),
            context={},
        )

    @staticmethod
    def from_dict(data: dict) -> "CalendlyWebhook":
        return from_dict(CalendlyWebhook, data)

    @property
    def is_invitee_created(self) -> bool:
        return self.event == CalendlyEventType.INVITEE_CREATED

    @property
    def is_invitee_canceled(self) -> bool:
        return self.event == CalendlyEventType.INVITEE_CANCELED

    @property
    def thread_id(self) -> Optional[str]:
        """The calendly component will put the thread_id in utmContent"""
        return self.decode_utm_content(self.payload.tracking.utm_content)[0]

    @property
    def user_id(self) -> Optional[str]:
        """The calendly component will put the user_id in utmContent"""
        return self.decode_utm_content(self.payload.tracking.utm_content)[1]

    @property
    def booking_id(self) -> Optional[str]:
        """The calendly component will put the booking_id in utmContent
        booking_id is optional.
        """
        return self.decode_utm_content(self.payload.tracking.utm_content)[2]

    @staticmethod
    def decode_utm_content(
        utm_content: str,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """The calendly component will put the thread_id:user_id in utmContent"""
        if utm_content is None:
            return None, None, None
        parts = utm_content.split(":")
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            return parts[0], parts[1], None
        else:
            return None, None, None

    @staticmethod
    def encode_utm_content(
        thread_id: str, user_id: str, booking_id: str = None
    ):
        if booking_id is None:
            return f"{thread_id}:{user_id}"
        else:
            return f"{thread_id}:{user_id}:{booking_id}"


@dataclass
class CalendlyEventV2:
    uri: str
    name: str
    status: str
    start_time: str
    end_time: str
    event_type: str
    location: Dict[str, Any]
    invitees_counter: Dict[str, Any]
    created_at: str
    updated_at: str
    event_memberships: List[Any]
    event_guests: List[Any]


@dataclass
class CalendlyGetEventResponse:
    resource: CalendlyEventV2
