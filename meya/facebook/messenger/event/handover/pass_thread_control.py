from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from typing import Any
from typing import Dict


@dataclass
class FacebookMessengerPassThreadControlEvent(WebhookEvent):
    new_owner_app_id: int = entry_field()
    metadata: Dict[str, Any] = entry_field(
        sensitive=True, default_factory=dict
    )
