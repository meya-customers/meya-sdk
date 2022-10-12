from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.payload.order import Order
from meya.shopify.payload.order import OrderMeyaStatus
from typing import List


@dataclass
class ShopifyOrderStatusComponent(BaseApiComponent):
    """
    Get order status
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: OrderMeyaStatus = response_field(sensitive=True)

    order: Order = element_field(help="Order element")

    async def start(self) -> List[Entry]:
        return self.respond(data=self.Response(result=self.order.status))
