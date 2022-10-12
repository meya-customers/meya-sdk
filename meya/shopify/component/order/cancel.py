from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.order import CancelReason
from meya.shopify.payload.order import Order
from typing import List
from typing import Optional


@dataclass
class ShopifyOrderCancelComponent(BaseApiComponent):
    """
    Cancel order
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: Order = response_field(sensitive=True)

    order_id: int = element_field(help="Order ID")
    notify: bool = element_field(default=False, help="Notify user by email")
    reason: Optional[CancelReason] = element_field(
        default=None, help="Cancel reason"
    )
    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.order_cancel(
                order_id=self.order_id, reason=self.reason, notify=self.notify
            )
            return self.respond(data=self.Response(result=response))
