from dataclasses import dataclass
from meya.data_collection.time_zone import TimeZoneData
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import ClassVar
from typing import Optional


@dataclass
class LocationData(Payload):
    DEFAULT_SCOPE: ClassVar = None

    latitude: Optional[float] = payload_field(default=None)
    longitude: Optional[float] = payload_field(default=None)
    time_zone: Optional[TimeZoneData] = payload_field(default=None)
    city: Optional[str] = payload_field(default=None)
    region: Optional[str] = payload_field(default=None)
    country: Optional[str] = payload_field(default=None)
    country_flag_emoji: Optional[str] = payload_field(default=None)
