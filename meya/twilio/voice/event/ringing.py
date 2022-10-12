from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from meya.twilio.voice.payload.webhook import TwilioVoiceWebhookPayload


@dataclass
class TwilioVoiceRingingEvent(WebhookEvent):
    payload: TwilioVoiceWebhookPayload = entry_field(sensitive=True)
