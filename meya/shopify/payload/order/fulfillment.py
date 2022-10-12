from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.shopify.payload.order.line_item import LineItem
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


@dataclass
class FulfillmentStatus(SimpleEnum):
    PENDING = "pending"
    OPEN = "open"
    SUCCESS = "success"
    CANCELLED = "cancelled"
    ERROR = "error"
    FAILURE = "failure"


class ShipmentStatus(SimpleEnum):
    LABEL_PRINTED = "label_printed"
    LABEL_PURCHASED = "label_purchased"
    ATTEMPTED_DELIVERY = "attempted_delivery"
    READY_FOR_PICKUP = "ready_for_pickup"
    CONFIRMED = "confirmed"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILURE = "failure"


@dataclass
class Fulfillment(Payload):
    id: int = payload_field()
    order_id: int = payload_field()
    created_at: str = payload_field()
    service: str = payload_field()
    updated_at: str = payload_field()
    location_id: int = payload_field()
    line_items: List[LineItem] = payload_field()
    tracking_company: Optional[str] = payload_field(default=None)
    shipment_status: Optional[ShipmentStatus] = payload_field(default=None)
    status: Optional[FulfillmentStatus] = payload_field(default=None)
    tracking_numbers: Optional[List[str]] = payload_field(default=None)
    tracking_urls: Optional[List[str]] = payload_field(default=None)
