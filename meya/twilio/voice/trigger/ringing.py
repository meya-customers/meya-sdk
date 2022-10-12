from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.twilio.voice.event.ringing import TwilioVoiceRingingEvent
from meya.twilio.voice.payload.webhook import TwilioVoiceWebhookDirection
from meya.twilio.voice.payload.webhook import TwilioVoiceWebhookPayload


@dataclass
class TwilioVoiceRingingTrigger(WebhookTrigger):
    direction: TwilioVoiceWebhookDirection = element_field()
    encrypted_entry: TwilioVoiceRingingEvent = process_field()
    entry: TwilioVoiceRingingEvent = process_field()

    @dataclass
    class Response:
        result: TwilioVoiceWebhookPayload = response_field(sensitive=True)
