from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import Optional


@dataclass
class FrontPayload(Payload):
    pass


@dataclass
class FrontPagination(FrontPayload):
    next: Optional[str] = payload_field(default=None)


@dataclass
class FrontBaseResponse(FrontPayload):
    conversation_reference: str = payload_field()
    message_uid: str = payload_field()
    status: str = payload_field()
    conversation_id: Optional[str] = payload_field(default=None)
