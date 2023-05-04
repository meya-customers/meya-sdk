from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import List
from typing import Optional


@dataclass
class ZendeskHelpCenterLabel(Payload):
    created_at: Optional[int] = payload_field(default=None)
    id: Optional[int] = payload_field(default=None)
    name: str = payload_field()
    updated_at: Optional[str] = payload_field(default=None)
    url: Optional[str] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterLabelsResponse(Payload):
    labels: List[ZendeskHelpCenterLabel] = payload_field(default_factory=list)
