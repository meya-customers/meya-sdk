from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


class ProductStatus(SimpleEnum):
    ACTIVE = "active"
    DRAFT = "draft"
    ARCHIVED = "archived"


@dataclass
class Image(Payload):
    id: int = payload_field()
    src: str = payload_field()
    width: int = payload_field()
    height: int = payload_field()
    position: int = payload_field()
    created_at: str = payload_field()
    product_id: int = payload_field()
    updated_at: str = payload_field()
    admin_graphql_api_id: str = payload_field()
    alt: Optional[str] = payload_field(default=None)
    variants_ids: Optional[List[int]] = payload_field(default=None)


@dataclass
class Price:
    currency_code: str = payload_field()
    amount: float = payload_field()


@dataclass
class PresentmentPrice:
    price: List[Price] = payload_field()
    compare_at_price: Optional[float] = payload_field()


@dataclass
class Variants(Payload):
    id: int = payload_field()
    product_id: int = payload_field()
    requires_shipping: bool = payload_field()
    sku: str = payload_field()
    taxable: bool = payload_field()
    title: str = payload_field()
    updated_at: str = payload_field()
    inventory_item_id: int = payload_field()
    inventory_management: str = payload_field()
    barcode: str = payload_field()
    inventory_policy: str = payload_field()
    inventory_quantity: int = payload_field()
    option1: str = payload_field()
    position: int = payload_field()
    price: float = payload_field()
    created_at: str = payload_field()
    fulfillment_service: str = payload_field()
    grams: float = payload_field()
    weight: float = payload_field()
    weight_unit: str = payload_field()
    compare_at_price: Optional[float] = payload_field(default=None)
    presentment_prices: Optional[List[PresentmentPrice]] = payload_field(
        default=None
    )


@dataclass
class Option(Payload):
    id: int = payload_field()
    product_id: int = payload_field()
    name: str = payload_field()
    position: int = payload_field()
    values: Optional[List[str]] = payload_field(default=None)


@dataclass
class BaseProduct(Payload):
    id: int = payload_field()
    title: str = payload_field()
    vendor: str = payload_field()
    product_id: Optional[int] = payload_field(default=None)


@dataclass
class Product(BaseProduct):
    tags: str = payload_field()
    handle: str = payload_field()
    status: ProductStatus = payload_field()
    body_html: str = payload_field()
    product_type: str = payload_field()
    created_at: str = payload_field()
    updated_at: str = payload_field()
    published_at: str = payload_field()
    published_scope: str = payload_field()
    variants: Optional[List[Variants]] = payload_field(default=None)
    options: Optional[List[Option]] = payload_field(default=None)
    template_suffix: Optional[str] = payload_field(default=None)
    images: Optional[List[Image]] = payload_field(default=None)
    image: Optional[Image] = payload_field(default=None)
    admin_graphql_api_id: Optional[str] = payload_field(default=None)
