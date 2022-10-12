from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontTrashConversationEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontTrashEvent(WebhookEvent):
    payload: FrontTrashConversationEvent = entry_field(sensitive=True)
