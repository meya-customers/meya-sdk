from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.customer import Customer
from typing import List


@dataclass
class ShopifyCustomerGetComponent(BaseApiComponent):
    """
    Get customer by ID
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: Customer = response_field(sensitive=True)

    customer_id: int = element_field(help="Customer ID")
    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.customer_get(
                customer_id=self.customer_id
            )
            return self.respond(data=self.Response(result=response))
