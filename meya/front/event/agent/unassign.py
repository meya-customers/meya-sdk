from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontUnassignEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontAgentUnassignEvent(WebhookEvent):
    payload: FrontUnassignEvent = entry_field(sensitive=True)
