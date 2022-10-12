from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.zendesk.support.payload import ZendeskSupportPayload
from typing import Any


@dataclass
class ZendeskSupportTicketFieldPair(ZendeskSupportPayload):
    id: int = payload_field()
    value: Any = payload_field(default=None)
