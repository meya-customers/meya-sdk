from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import Optional


@dataclass
class ZendeskHelpCenterBaseResponse(Payload):
    count: int = payload_field()
    page: int = payload_field()
    page_count: int = payload_field()
    per_page: int = payload_field()
    sort_by: Optional[str] = payload_field(default=None)
    sort_order: Optional[str] = payload_field(default=None)
    previous_page: Optional[str] = payload_field(default=None)
    next_page: Optional[str] = payload_field(default=None)
