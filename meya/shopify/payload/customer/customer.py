from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.shopify.payload.address import Address
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


class MarketOptIn(SimpleEnum):
    SINGLE_OPT_IN = "single_opt_in"
    CONFIRMED_OPT_INT = "confirmed_opt_in"
    UNKNOWN = "unknown"


class CustomerState(SimpleEnum):
    DISABLED = "disabled"
    INVITED = "invited"
    ENABLED = "enabled"


@dataclass
class Customer(Payload):
    id: int = payload_field()
    accepts_marketing: bool = payload_field()
    created_at: str = payload_field()
    updated_at: str = payload_field()
    first_name: str = payload_field()
    last_name: str = payload_field()
    orders_count: int = payload_field()
    state: CustomerState = payload_field()
    total_spent: str = payload_field()
    verified_email: bool = payload_field()
    currency: str = payload_field()
    accepts_marketing_updated_at: str = payload_field()
    admin_graphql_api_id: str = payload_field()
    tax_exempt: Optional[bool] = payload_field(default=None)
    default_address: Optional[Address] = payload_field(default=None)
    tags: Optional[str] = payload_field(default=None)
    addresses: Optional[List[Address]] = payload_field(default=None)
    last_order_name: Optional[str] = payload_field(default=None)
    tax_exemptions: Optional[list] = payload_field(default=None)
    multipass_identifier: Optional[str] = payload_field(default=None)
    note: Optional[str] = payload_field(default=None)
    email: Optional[str] = payload_field(default=None)
    phone: Optional[str] = payload_field(default=None)
    last_order_id: Optional[int] = payload_field(default=None)
    marketing_opt_in_level: Optional[MarketOptIn] = payload_field(default=None)
