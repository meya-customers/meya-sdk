from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.order import Order
from typing import List


@dataclass
class ShopifyUpdateShippingAddressComponent(BaseApiComponent):
    """
    Update shipping address
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: Order = response_field(sensitive=True)

    order_id: int = element_field(help="Order ID")
    address: str = element_field(help="New address")
    address_2: str = element_field(help="New address 2")
    postal_code: str = element_field(help="New postal code")
    city: str = element_field(help="New city")
    country: str = element_field(help="New country")
    province: str = element_field(help="New province")

    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        with ShopifyIntegration.current.set(integration):
            response = await integration.order_update_shipping_address(
                order_id=self.order_id,
                address=self.address,
                address_2=self.address_2,
                postal_code=self.postal_code,
                city=self.city,
                country=self.country,
                province=self.province,
            )
            return self.respond(data=self.Response(result=response))
