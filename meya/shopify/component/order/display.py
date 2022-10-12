from dataclasses import dataclass
from meya.button.spec import ButtonElementSpec
from meya.component.element import Component
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.shopify.integration.integration import ShopifyIntegration
from meya.shopify.integration.integration import ShopifyIntegrationRef
from meya.shopify.payload.order import Order
from meya.shopify.payload.order import OrderMeyaStatus
from meya.tile.spec import TileCell
from meya.tile.spec import TileElementSpec
from meya.tile.spec import TileImage
from typing import List
from typing import Optional


@dataclass
class ShopifyOrderDisplayComponent(Component):
    """
    Display orders as tiles
    """

    @dataclass
    class Response:
        result: List[TileElementSpec] = response_field(sensitive=True)

    orders: List[Order] = element_field(help="List of orders")
    select_button_text: str = element_field(
        default="Select", help="Set button text"
    )
    price_cell_text: str = element_field(
        default="Price", help="Set top tile cell text"
    )
    status_cell_text: str = element_field(
        default="Status", help="Set bottom tile cell text"
    )
    filter: Optional[List[OrderMeyaStatus]] = element_field(
        default=None, help="Filter list of status"
    )
    integration: ShopifyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ShopifyIntegration = await self.resolve(self.integration)
        tiles = []
        for order in self.orders:
            order_status = order.status
            if self.filter and order_status not in self.filter:
                continue

            button = ButtonElementSpec(
                text=self.select_button_text, result=order
            )
            line_item = order.line_items[0]

            with ShopifyIntegration.current.set(integration):
                product = await integration.product_get(
                    product_id=line_item.product_id
                )
            if product:
                tile = TileElementSpec(
                    title=product.title,
                    image=TileImage(url=product.image.src),
                    rows=[
                        [
                            TileCell(
                                cell=self.price_cell_text,
                                value="${:,.2f}".format(
                                    float(product.variants[0].price)
                                ),
                            ),
                            TileCell(
                                cell=self.status_cell_text, value=order_status
                            ),
                        ]
                    ],
                    buttons=[button],
                )

                tiles.append(tile)

        return self.respond(data=self.Response(result=tiles))
