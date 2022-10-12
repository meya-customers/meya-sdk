from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontReopenConversationEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontReopenEvent(WebhookEvent):
    payload: FrontReopenConversationEvent = entry_field(sensitive=True)
