from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontRestoreConversationEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontRestoreEvent(WebhookEvent):
    payload: FrontRestoreConversationEvent = entry_field(sensitive=True)
