from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import Optional


@dataclass
class Address(Payload):
    address1: str = payload_field()
    city: str = payload_field()
    province: str = payload_field()
    country: str = payload_field()
    last_name: str = payload_field()
    country_code: str = payload_field()
    province_code: str = payload_field()
    zip: Optional[str] = payload_field(default=None)
    first_name: Optional[str] = payload_field(default=None)
    phone: Optional[str] = payload_field(default=None)
    company: Optional[str] = payload_field(default=None)
    address2: Optional[str] = payload_field(default=None)
    latitude: Optional[float] = payload_field(default=None)
    longitude: Optional[float] = payload_field(default=None)
    name: Optional[str] = payload_field(default=None)
