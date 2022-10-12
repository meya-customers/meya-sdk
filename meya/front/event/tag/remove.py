from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.tag import FrontTagTargetData
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontTagRemoveEvent(WebhookEvent):
    payload: FrontTagTargetData = entry_field(sensitive=True)
