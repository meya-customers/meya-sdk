from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.order import Order
from meya.shopify.payload.order import RefundResponse
from typing import List


@dataclass
class ShopifyOrderRefundComponent(BaseApiComponent):
    """
    Refund order
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: RefundResponse = response_field(sensitive=True)

    order: Order = element_field(help="Order element")
    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.order_refund(order=self.order)
            return self.respond(data=self.Response(result=response))
