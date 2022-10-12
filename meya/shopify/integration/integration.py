from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from http import HTTPStatus
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.entry import Entry
from meya.integration.element.interactive import InteractiveIntegration
from meya.shopify.integration.api import ShopifyApi
from meya.shopify.payload.carrier_service import CarrierServiceCreateResponse
from meya.shopify.payload.customer import Customer
from meya.shopify.payload.order import CalculateRefund
from meya.shopify.payload.order import CancelReason
from meya.shopify.payload.order import Order
from meya.shopify.payload.order import OrderFilterFinancialStatus
from meya.shopify.payload.order import OrderFilterFulfillmentStatus
from meya.shopify.payload.order import OrderFilterStatus
from meya.shopify.payload.order import RefundResponse
from meya.shopify.payload.product import Product
from typing import ClassVar
from typing import List
from typing import Type


@dataclass
class ShopifyIntegration(InteractiveIntegration):
    """
    ## Setup

    ### Create shopify store
    ### Create new private app:

        `https://YOUR_STORE_URL/admin/apps/private`
    ### Grant full access
    ### Add keys to integration parameters
    """

    NAME: ClassVar[str] = "shopify"
    api_key: str = element_field(help="Shopify private app API key")
    password: str = element_field(help="Shopify private app password")
    store_url: str = element_field(help="Shopify store URL")

    async def rx(self) -> List[Entry]:
        """Mocked response"""
        return self.build_carrier_response()

    async def tx(self) -> List[Entry]:
        return []

    async def product_get(self, product_id: int) -> Product:
        response = await self.api.product_get(product_id)
        return Product.from_dict(response.data.get("product"))

    async def product_list(self) -> List[Product]:
        response = await self.api.product_list()
        return [
            Product.from_dict(product)
            for product in response.data.get("products")
        ]

    async def order_get(self, order_id: int) -> Order:
        response = await self.api.order_get(order_id)
        return Order.from_dict(response.data.get("order"))

    async def customer_get(self, customer_id: int) -> Customer:
        response = await self.api.customer_get(customer_id)
        return Customer.from_dict(response.data.get("customer"))

    async def customer_order_list(
        self,
        customer_id: int,
        ids: List[int] = None,
        status: OrderFilterStatus = None,
        fulfillment_status: OrderFilterFulfillmentStatus = None,
        financial_status: OrderFilterFinancialStatus = None,
    ) -> List[Order]:
        response = await self.api.customer_order_list(
            customer_id,
            ids,
            status.value,
            fulfillment_status.value,
            financial_status.value,
        )
        return [
            Order.from_dict(order) for order in response.data.get("orders")
        ]

    async def customer_search(self, email: str) -> List[Customer]:
        response = await self.api.customer_search(email)

        return [
            Customer.from_dict(customer)
            for customer in response.data.get("customers")
        ]

    async def order_cancel(
        self, order_id: int, reason: CancelReason, notify: bool
    ) -> Order:
        response = await self.api.order_cancel(order_id, reason, notify)
        return Order.from_dict(response.data.get("order"))

    async def order_open(self, order_id: int) -> Order:
        response = await self.api.order_open(order_id)
        return Order.from_dict(response.data.get("order"))

    async def order_close(self, order_id: int) -> Order:
        response = await self.api.order_close(order_id)
        return Order.from_dict(response.data.get("order"))

    async def carrier_service_create(
        self, name: str
    ) -> CarrierServiceCreateResponse:
        response = await self.api.carrier_service_create(
            name, self.gateway_webhook_url
        )
        return CarrierServiceCreateResponse.from_dict(
            response.data.get("carrier_service")
        )

    async def order_refund(self, order: Order) -> RefundResponse:
        calculate_refund_response = await self.order_calculate_refund(order)
        if calculate_refund_response:
            response = await self.api.order_refund(
                order.id, calculate_refund_response
            )
            return RefundResponse.from_dict(response.data)

    async def order_calculate_refund(self, order: Order) -> CalculateRefund:
        response = await self.api.calculate_refund(order)
        calculate_refund = CalculateRefund.from_dict(response.data)
        for transaction in calculate_refund.refund.get("transactions"):
            # https://shopify.dev/docs/admin-api/rest/reference/orders/refund
            transaction["kind"] = "refund"

        return calculate_refund

    async def order_update_shipping_address(
        self,
        order_id: int,
        address: str,
        address_2: str,
        postal_code: str,
        city: str,
        country: str,
        province: str,
    ) -> Order:
        response = await self.api.order_update_shipping_address(
            order_id, address, address_2, postal_code, city, country, province
        )
        return Order.from_dict(response.data.get("order"))

    @property
    def api(self) -> ShopifyApi:
        return ShopifyApi(
            store_url=self.store_url,
            api_key=self.api_key,
            password=self.password,
        )

    def build_carrier_response(self) -> List[Entry]:
        return self.respond(
            status=HTTPStatus.OK,
            data={
                "rates": [
                    {
                        "service_name": "Meya Test Carrier Service",
                        "service_code": "ZZ",
                        "total_price": "1295",
                        "description": "This is the fastest option by far",
                        "currency": "CAD",
                        "min_delivery_date": self.get_delivery_time(5),
                        "max_delivery_date": self.get_delivery_time(8),
                    }
                ]
            },
        )

    @staticmethod
    def get_delivery_time(days: int) -> str:
        return (
            (datetime.now() + timedelta(days=days))
            .astimezone()
            .strftime("%Y-%m-%d %H:%M:%S %z")
        )


class ShopifyIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = ShopifyIntegration
