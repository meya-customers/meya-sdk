from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.carrier_service import CarrierServiceCreateResponse
from typing import List


@dataclass
class ShopifyCarrierServiceCreateComponent(BaseApiComponent):
    """
    Create carrier service for this integration
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: CarrierServiceCreateResponse = response_field(sensitive=True)

    name: str = element_field(help="Carrier service name")
    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.carrier_service_create(name=self.name)
            return self.respond(data=self.Response(result=response))
