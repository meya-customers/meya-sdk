from meya.shopify.payload.product import Image
from meya.shopify.payload.product import Option
from meya.shopify.payload.product import Product
from meya.shopify.payload.product import ProductStatus
from meya.shopify.payload.product import Variants

variant = {
    "id": 37975218716872,
    "sku": "",
    "grams": 100,
    "price": "15000.00",
    "title": "Default Title",
    "weight": 0.1,
    "barcode": "",
    "option1": "Default Title",
    "option2": None,
    "option3": None,
    "taxable": True,
    "image_id": None,
    "position": 1,
    "created_at": "2021-02-01T19:17:37-03:00",
    "product_id": 6219189092552,
    "updated_at": "2021-02-02T10:30:27-03:00",
    "weight_unit": "kg",
    "compare_at_price": None,
    "inventory_policy": "deny",
    "inventory_item_id": 40069250678984,
    "requires_shipping": True,
    "inventory_quantity": 5,
    "fulfillment_service": "manual",
    "admin_graphql_api_id": "gid://shopify/ProductVariant/37975218716872",
    "inventory_management": "shopify",
    "old_inventory_quantity": 5,
}

image = {
    "id": 23651666526408,
    "alt": None,
    "src": "https://cdn.shopify.com/s/files/1/0533/7412/4232/products/gtx3090.jpg?v=1612217859",
    "width": 335,
    "height": 151,
    "position": 1,
    "created_at": "2021-02-01T19:17:39-03:00",
    "product_id": 6219189092552,
    "updated_at": "2021-02-01T19:17:39-03:00",
    "variant_ids": [],
    "admin_graphql_api_id": "gid://shopify/ProductImage/23651666526408",
}


def test_product_from_dict():
    assert Product.from_dict(
        {
            "id": 6219189092552,
            "tags": "",
            "image": image,
            "title": "GTX 3090",
            "handle": "gtx-3090",
            "images": [image],
            "status": "active",
            "vendor": "meyadev",
            "options": [
                {
                    "id": 7941145395400,
                    "name": "Title",
                    "values": ["Default Title"],
                    "position": 1,
                    "product_id": 6219189092552,
                }
            ],
            "variants": [variant],
            "body_html": "",
            "created_at": "2021-02-01T19:17:37-03:00",
            "updated_at": "2021-02-02T11:33:02-03:00",
            "product_type": "",
            "published_at": "2021-02-02T10:21:38-03:00",
            "published_scope": "web",
            "template_suffix": "",
            "admin_graphql_api_id": "gid://shopify/Product/6219189092552",
        }
    ) == Product(
        id=6219189092552,
        title="GTX 3090",
        vendor="meyadev",
        handle="gtx-3090",
        status=ProductStatus.ACTIVE,
        options=[
            Option.from_dict(
                {
                    "id": 7941145395400,
                    "name": "Title",
                    "values": ["Default Title"],
                    "position": 1,
                    "product_id": 6219189092552,
                }
            )
        ],
        tags="",
        image=Image.from_dict(image),
        images=[Image.from_dict(image)],
        variants=[Variants.from_dict(variant)],
        body_html="",
        created_at="2021-02-01T19:17:37-03:00",
        updated_at="2021-02-02T11:33:02-03:00",
        product_type="",
        published_at="2021-02-02T10:21:38-03:00",
        published_scope="web",
        template_suffix="",
        admin_graphql_api_id="gid://shopify/Product/6219189092552",
    )
