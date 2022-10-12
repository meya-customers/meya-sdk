from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.http.payload.field import payload_field
from typing import List
from typing import Optional


@dataclass
class FrontRule(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()
    is_private: bool = payload_field()
    actions: Optional[List[str]] = payload_field(default=None)
