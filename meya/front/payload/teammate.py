from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.front.payload.payload import FrontPagination
from meya.http.payload.field import payload_field
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


"""
https://dev.frontapp.com/reference/teammates
"""


@dataclass
class FrontTeammateGet(FrontPayload):
    id: str = payload_field()
    first_name: str = payload_field()
    email: str = payload_field()
    custom_fields: Optional[Dict[str, Any]] = payload_field(
        default_factory=dict
    )
    last_name: Optional[str] = payload_field(default=None)
    username: Optional[str] = payload_field(default=None)
    is_admin: Optional[bool] = payload_field(default=None)
    is_available: Optional[bool] = payload_field(default=None)
    is_blocked: Optional[bool] = payload_field(default=None)


@dataclass
class FrontTeammateList(FrontPayload):
    pagination: FrontPagination = payload_field(key="_pagination")
    results: Optional[List[FrontTeammateGet]] = payload_field(
        key="_results", default_factory=list
    )
