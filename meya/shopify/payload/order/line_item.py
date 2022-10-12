from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.shopify.payload.product import BaseProduct
from typing import List
from typing import Optional


@dataclass
class LineItem(BaseProduct):
    sku: str = payload_field()
    name: str = payload_field()
    grams: int = payload_field()
    duties: list = payload_field()
    taxable: bool = payload_field()
    quantity: int = payload_field()
    gift_card: bool = payload_field()
    price: str = payload_field()
    tax_lines: List[dict] = payload_field()
    properties: list = payload_field()
    variant_id: int = payload_field()
    product_exists: bool = payload_field()
    total_discount: str = payload_field()
    requires_shipping: bool = payload_field()
    fulfillment_service: str = payload_field()
    admin_graphql_api_id: str = payload_field()
    discount_allocations: list = payload_field()
    fulfillable_quantity: int = payload_field()
    variant_inventory_management: str = payload_field()
    total_discount_set: Optional[dict] = payload_field(default=None)
    fulfillment_status: Optional[str] = payload_field(default=None)
    variant_title: Optional[str] = payload_field(default=None)
    price_set: Optional[dict] = payload_field(default=None)
    origin_location: Optional[dict] = payload_field(default=None)
