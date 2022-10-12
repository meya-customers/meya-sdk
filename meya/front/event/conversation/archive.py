from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.event import FrontArchiveConversationEvent
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontArchiveEvent(WebhookEvent):
    payload: FrontArchiveConversationEvent = entry_field(sensitive=True)
