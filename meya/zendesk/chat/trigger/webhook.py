from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.zendesk.chat.event.webhook import ZendeskChatWebhookEvent
from typing import Any
from typing import Dict


@dataclass
class ZendeskChatWebhookTrigger(WebhookTrigger):
    zendesk_chat_event_type: str = element_field(signature=True)

    entry: ZendeskChatWebhookEvent = process_field()
    encrypted_entry: ZendeskChatWebhookEvent = process_field()

    @dataclass
    class Response:
        session_id: str = response_field()
        result: Dict[str, Any] = response_field(sensitive=True)
