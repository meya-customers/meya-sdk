from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import Optional


@dataclass
class TimeZoneData(Payload):
    name: Optional[str] = payload_field(default=None)
    gmt_offset: Optional[int] = payload_field(default=None)
    code: Optional[str] = payload_field(default=None)
    is_daylight_saving: Optional[bool] = payload_field(default=None)
