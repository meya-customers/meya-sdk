from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import List


@dataclass
class SalesforceQueryRequest(Payload):
    q: str = payload_field()


@dataclass
class SalesforceQueryResponse(Payload):
    to_camel_case_fields = True
    total_size: int = payload_field()
    done: bool = payload_field
    records: List[dict] = payload_field(default_factory=list)
