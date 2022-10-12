from dataclasses import dataclass
from meya.directly.payload.payload import DirectlyWebhookPayload
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent


@dataclass
class DirectlyWebhookEvent(WebhookEvent):
    payload: DirectlyWebhookPayload = entry_field(sensitive=True)
