from dataclasses import dataclass
from meya.directly.event.webhook import DirectlyWebhookEvent
from meya.directly.payload.payload import DirectlyWebhookPayload
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class DirectlyWebhookTrigger(WebhookTrigger):
    # this is not validated, but should match
    # meya.directly.integration.payload.EventType
    directly_event_type: str = element_field(signature=True)

    entry: DirectlyWebhookEvent = process_field()
    encrypted_entry: DirectlyWebhookEvent = process_field()

    @dataclass
    class Response:
        result: DirectlyWebhookPayload = response_field()

    async def match(self) -> TriggerMatchResult:
        if self.entry.payload.event_type == self.directly_event_type:
            return self.succeed(
                data=self.Response(self.encrypted_entry.payload)
            )
        else:
            return self.fail()
