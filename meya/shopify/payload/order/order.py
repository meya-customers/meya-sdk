from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.shopify.payload.address import Address
from meya.shopify.payload.customer import Customer
from meya.shopify.payload.order.fulfillment import Fulfillment
from meya.shopify.payload.order.fulfillment import LineItem
from meya.shopify.payload.order.fulfillment import ShipmentStatus
from meya.shopify.payload.order.refund import RestockType
from meya.shopify.payload.order.transaction import Transaction
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


class OrderMeyaStatus(SimpleEnum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    PARTIALLY_REFUNDED = "partially_refunded"
    REFUNDED = "refunded"
    VOIDED = "voided"
    LABEL_PRINTED = "label_printed"
    LABEL_PURCHASED = "label_purchased"
    ATTEMPTED_DELIVERY = "attempted_delivery"
    READY_FOR_PICKUP = "ready_for_pickup"
    CONFIRMED = "confirmed"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILURE = "failure"


class OrderFilterStatus(SimpleEnum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    ANY = "any"


class OrderFilterFulfillmentStatus(SimpleEnum):
    SHIPPED = "shipped"
    PARTIAL = "partial"
    UNSHIPPED = "unshipped"
    ANY = "any"
    UNFULFILLED = "unfulfilled"


class OrderFilterFinancialStatus(SimpleEnum):
    AUTHORIZED = "authorized"
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    REFUNDED = "refunded"
    VOIDED = "voided"
    PARTIALLY_REFUNDED = "partially_refunded"
    ANY = "any"
    UNPAID = "unpaid"


class CancelReason(SimpleEnum):
    CUSTOMER = "customer"
    FRAUD = "fraud"
    INVENTORY = "inventory"
    DECLINED = "declined"
    OTHER = "other"


class FinancialStatus(SimpleEnum):
    AUTHORIZED = "authorized"
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    REFUNDED = "refunded"
    VOIDED = "voided"
    PARTIALLY_REFUNDED = "partially_refunded"


class OrderFulfillmentStatus(SimpleEnum):
    FULFILLED = "fulfilled"
    PARTIAL = "partial"
    NULL = "null"
    RESTOCKED = "restocked"


class ProcessingMethod(SimpleEnum):
    CHECKOUT = "checkout"
    DIRECT = "direct"
    MANUAL = "manual"
    OFFSITE = "offsite"
    EXPRESS = "express"
    FREE = "free"


@dataclass
class Discount:
    code: str = payload_field()
    amount: str = payload_field()
    type: str = payload_field()


@dataclass
class Order(Payload):
    app_id: int = payload_field()
    line_items: List[LineItem] = payload_field()
    buyer_accepts_marketing: bool = payload_field()
    created_at: str = payload_field()
    currency: str = payload_field()
    customer: Customer = payload_field()
    email: str = payload_field()
    financial_status: FinancialStatus = payload_field()
    id: int = payload_field()
    name: str = payload_field()
    note: str = payload_field()
    note_attributes: List[dict] = payload_field()
    number: int = payload_field()
    order_number: int = payload_field()
    payment_gateway_names: List[str] = payload_field()
    presentment_currency: str = payload_field()
    processed_at: str = payload_field()
    processing_method: ProcessingMethod = payload_field()
    refunds: List[dict] = payload_field()
    subtotal_price: str = payload_field()
    tax_lines: List[dict] = payload_field()
    taxes_included: bool = payload_field()
    test: bool = payload_field()
    token: str = payload_field()
    total_discounts: str = payload_field()
    total_line_items_price: str = payload_field()
    total_price: str = payload_field()
    total_tax: str = payload_field()
    total_tip_received: str = payload_field()
    total_weight: int = payload_field()
    updated_at: str = payload_field()
    user_id: int = payload_field()
    order_status_url: str = payload_field()
    total_price_usd: str = payload_field()
    admin_graphql_api_id: str = payload_field()
    payment_details: Optional[dict] = payload_field(default=None)
    total_line_items_price_set: Optional[dict] = payload_field(default=None)
    total_price_set: Optional[dict] = payload_field(default=None)
    total_shipping_price_set: Optional[dict] = payload_field(default=None)
    total_discounts_set: Optional[dict] = payload_field(default=None)
    total_tax_set: Optional[dict] = payload_field(default=None)
    subtotal_price_set: Optional[dict] = payload_field(default=None)
    client_details: Optional[dict] = payload_field(default=None)
    checkout_token: Optional[str] = payload_field(default=None)
    cart_token: Optional[str] = payload_field(default=None)
    browser_ip: Optional[str] = payload_field(default=None)
    current_total_price: Optional[str] = payload_field(default=None)
    current_subtotal_price: Optional[str] = payload_field(default=None)
    current_total_tax: Optional[str] = payload_field(default=None)
    total_outstanding: Optional[str] = payload_field(default=None)
    source_identifier: Optional[str] = payload_field(default=None)
    source_url: Optional[str] = payload_field(default=None)
    reference: Optional[str] = payload_field(default=None)
    device_id: Optional[int] = payload_field(default=None)
    fulfillments: Optional[List[Fulfillment]] = payload_field(default=None)
    discount_applications: Optional[List[dict]] = payload_field(default=None)
    discount_codes: Optional[List[dict]] = payload_field(default=None)
    current_total_tax_set: Optional[dict] = payload_field(default=None)
    current_subtotal_price_set: Optional[dict] = payload_field(default=None)
    current_total_price_set: Optional[dict] = payload_field(default=None)
    current_total_discounts: Optional[str] = payload_field(default=None)
    current_total_discounts_set: Optional[dict] = payload_field(default=None)
    current_total_duties_set: Optional[dict] = payload_field(default=None)
    billing_address: Optional[Address] = payload_field(default=None)
    shipping_address: Optional[Address] = payload_field(default=None)
    transactions: Optional[List[Transaction]] = payload_field(default=None)
    closed_at: Optional[str] = payload_field(default=None)
    fulfillment_status: Optional[OrderFulfillmentStatus] = payload_field(
        default=None
    )
    phone: Optional[str] = payload_field(default=None)
    cancelled_at: Optional[str] = payload_field(default=None)
    landing_site: Optional[str] = payload_field(default=None)
    cancel_reason: Optional[CancelReason] = payload_field(default=None)
    referring_site: Optional[str] = payload_field(default=None)
    customer_locale: Optional[str] = payload_field(default=None)
    contact_email: Optional[str] = payload_field(default=None)
    original_total_duties_set: Optional[dict] = payload_field(default=None)
    tags: Optional[str] = payload_field(default=None)
    landing_site_ref: Optional[str] = payload_field(default=None)
    shipping_lines: Optional[List[dict]] = payload_field(default=None)
    location_id: Optional[int] = payload_field(default=None)

    def get_restock_type(self, line_item_id: int) -> RestockType:
        if not self.fulfillments:
            return RestockType.CANCEL.value

        for fulfillment in self.fulfillments:
            if (
                line_item_id
                in [line_item.id for line_item in fulfillment.line_items]
                and fulfillment.shipment_status
                == ShipmentStatus.DELIVERED.DELIVERED
            ):
                return RestockType.RETURN.value
        return RestockType.NO_RESTOCK.value

    @property
    def status(self) -> OrderMeyaStatus:
        if (
            self.fulfillments
            and self.fulfillments[0].shipment_status
            and self.financial_status
            not in [
                FinancialStatus.REFUNDED.value,
                FinancialStatus.VOIDED.value,
            ]
        ):
            return self.fulfillments[0].shipment_status.value

        return self.financial_status.value
