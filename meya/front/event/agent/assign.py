from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontAssignEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontAgentAssignEvent(WebhookEvent):
    payload: FrontAssignEvent = entry_field(sensitive=True)
