from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.zendesk.sunshine_conversations.payload import SunshinePayload
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class SunshineAppUser(SunshinePayload):
    _id: Optional[str] = payload_field(default=None, key="_id")
    user_id: Optional[str] = payload_field(default=None)
    conversation_started: Optional[bool] = payload_field(default=None)
    email: Optional[str] = payload_field(default=None)
    surname: Optional[str] = payload_field(default=None)
    given_name: Optional[str] = payload_field(default=None)
    signed_up_at: Optional[str] = payload_field(default=None)
    properties: Optional[Dict[str, Any]] = payload_field(default=None)
