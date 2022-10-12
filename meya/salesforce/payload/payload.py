from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import List


@dataclass
class SalesforceCreateObjectBaseResponse(Payload):
    id: str = payload_field()
    errors: List = payload_field(default_factory=list)
    success: bool = payload_field()
