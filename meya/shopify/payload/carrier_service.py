from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import List
from typing import Optional


@dataclass
class CarrierServiceCreateResponse(Payload):
    id: int = payload_field()
    name: str = payload_field()
    active: bool = payload_field()
    service_discovery: Optional[bool] = payload_field(default=None)
    carrier_service_type: Optional[str] = payload_field(default=None)
    admin_graphql_api_id: Optional[str] = payload_field(default=None)
    format: str = payload_field()
    callback_url: str = payload_field()


@dataclass
class CarrierServiceDetails(Payload):
    origin: dict = payload_field()
    destination: dict = payload_field()
    items: List[dict] = payload_field()
    currency: Optional[str] = payload_field()
    locale: Optional[str] = payload_field()


@dataclass
class CarrierService(Payload):
    rate: CarrierServiceDetails = payload_field()
