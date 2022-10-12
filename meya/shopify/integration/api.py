from dataclasses import dataclass
from http import HTTPStatus
from meya.db.view.http import HttpBasicAuth
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.shopify.payload.order import CalculateRefund
from meya.shopify.payload.order import CancelReason
from meya.shopify.payload.order import Order
from typing import Dict
from typing import List
from typing import Union

API_URL = "admin/api/2021-01"


@dataclass
class ShopifyApi(Api):
    store_url: str
    api_key: str
    password: str

    async def product_list(self) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/products/product#index-2021-01
        """
        return await self.get(
            f"{self.api_root}/products.json", {}, HTTPStatus.OK
        )

    async def product_get(self, product_id: int) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/products/product#show-2021-01
        """
        return await self.get(
            f"{self.api_root}/products/{product_id}.json", {}, HTTPStatus.OK
        )

    async def order_get(self, order_id: int) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/order#show-2021-01
        """
        return await self.get(
            f"{self.api_root}/orders/{order_id}.json?status=any",
            {},
            HTTPStatus.OK,
        )

    async def customer_get(self, customer_id: int) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/customers/customer#update-2021-01
        """
        return await self.get(
            f"{self.api_root}/customers/{customer_id}.json", {}, HTTPStatus.OK
        )

    async def customer_order_list(
        self,
        customer_id: int,
        ids: List[int] = None,
        status: str = None,
        fulfillment_status: str = None,
        financial_status: str = None,
    ) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/customers/customer#orders-2021-01
        """
        params = {
            "financial_status": financial_status,
            "fulfillment_status": fulfillment_status,
            "status": status,
        }
        if ids:
            params["query"] = ",".join(map(str, ids))

        return await self.get(
            f"{self.api_root}/customers/{customer_id}/orders.json?",
            params,
            HTTPStatus.OK,
        )

    async def customer_search(self, email: str) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/customers/customer#search-2021-01
        """
        return await self.get(
            f"{self.api_root}/customers/search.json",
            {"query": f"email:{email}"},
            HTTPStatus.OK,
        )

    async def order_cancel(
        self, order_id, reason: CancelReason, notify: bool
    ) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/order#cancel-2021-01
        """
        return await self.post(
            f"{self.api_root}/orders/{order_id}/cancel.json",
            {"reason": reason.value, "email": notify},
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def order_close(self, order_id) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/order#close-2021-01
        """
        return await self.post(
            f"{self.api_root}/orders/{order_id}/close.json",
            None,
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def order_open(self, order_id) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/order#open-2021-01
        """
        return await self.post(
            f"{self.api_root}/orders/{order_id}/open.json",
            None,
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def order_update_shipping_address(
        self,
        order_id: int,
        address: str,
        address_2: str,
        postal_code: str,
        city: str,
        country: str,
        province: str,
    ) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/order#update-2021-01
        """
        return await self.put(
            f"{self.api_root}/orders/{order_id}.json",
            {
                "order": {
                    "id": order_id,
                    "shipping_address": {
                        "city": city,
                        "address1": address,
                        "address2": address_2,
                        "postal_code": postal_code,
                        "country": country,
                        "province": province,
                    },
                }
            },
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def order_refund(
        self, order_id: int, calculated_refund: CalculateRefund
    ) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/refund#index-2021-01
        """
        return await self.post(
            f"{self.api_root}/orders/{order_id}/refunds.json",
            calculated_refund.to_dict(),
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def calculate_refund(self, order: Order) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/orders/refund#calculate-2021-01
        """
        return await self.post(
            f"{self.api_root}/orders/{order.id}/refunds/calculate.json",
            self.build_calculate_refund_payload(order),
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    async def carrier_service_create(
        self, name: str, gateway_url: str
    ) -> HttpResponseEntry:
        """
        https://shopify.dev/docs/admin-api/rest/reference/shipping-and-fulfillment/carrierservice
        """
        return await self.post(
            f"{self.api_root}/carrier_services.json",
            {
                "carrier_service": {
                    "name": name,
                    "callback_url": gateway_url,
                    "service_discovery": True,
                }
            },
            HTTPStatus.OK,
            HTTPStatus.CREATED,
        )

    @staticmethod
    def build_calculate_refund_payload(order: Order) -> dict:
        data = {
            "refund": {
                "shipping": {"full_refund": True},
                "refund_line_items": [],
            }
        }
        for line_item in order.line_items:
            data["refund"]["refund_line_items"].append(
                {
                    "line_item_id": line_item.id,
                    "quantity": line_item.quantity,
                    "restock_type": order.get_restock_type(line_item.id),
                    "location_id": order.location_id,
                }
            )

        return data

    async def post(
        self, url: str, json: Union[dict, None], *expected: int
    ) -> HttpResponseEntry:
        response = await self.http.post(url, json=json, auth=self.auth)
        response.check_status(*expected)
        return response

    async def put(
        self, url: str, json: dict, *expected: int
    ) -> HttpResponseEntry:
        response = await self.http.put(url, json=json, auth=self.auth)
        response.check_status(*expected)
        return response

    async def get(
        self, url: str, params: Dict, *expected: int
    ) -> HttpResponseEntry:
        response = await self.http.get(url, params=params, auth=self.auth)
        response.check_status(*expected)
        return response

    @property
    def api_root(self) -> str:
        return f"https://{self.store_url}/{API_URL}"

    @property
    def auth(self) -> HttpBasicAuth:
        return HttpBasicAuth(self.api_key, self.password)
