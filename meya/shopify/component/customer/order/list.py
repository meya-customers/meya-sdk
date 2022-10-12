from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.order import Order
from meya.shopify.payload.order import OrderFilterFinancialStatus
from meya.shopify.payload.order import OrderFilterFulfillmentStatus
from meya.shopify.payload.order import OrderFilterStatus
from typing import List
from typing import Optional


@dataclass
class ShopifyCustomerOrderListComponent(BaseApiComponent):
    """
    Get customer orders
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: List[Order] = response_field(sensitive=True)

    customer_id: int = element_field(help="Customer ID")
    integration: ShopifyIntegrationRef = element_field()
    ids: Optional[List[int]] = element_field(
        default=None, help="List of orders IDs"
    )
    financial_status: OrderFilterFinancialStatus = element_field(
        default=OrderFilterStatus.ANY, help="Financial status"
    )
    fulfillment_status: OrderFilterFulfillmentStatus = element_field(
        default=OrderFilterFulfillmentStatus.ANY, help="Fulfillment status"
    )
    status: OrderFilterStatus = element_field(
        default=OrderFilterStatus.OPEN, help="Order status"
    )

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.customer_order_list(
                customer_id=self.customer_id,
                ids=self.ids,
                status=self.status,
                financial_status=self.financial_status,
                fulfillment_status=self.fulfillment_status,
            )
            return self.respond(data=self.Response(result=response))
