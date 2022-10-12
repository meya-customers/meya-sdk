from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from typing import Any
from typing import Dict


@dataclass
class ZendeskChatWebhookEvent(WebhookEvent):
    session_id: str = entry_field()
    payload: Dict[str, Any] = entry_field(sensitive=True)
