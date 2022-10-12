from meya.shopify.payload.order import Order


def test_order_from_dict():
    try:
        Order.from_dict(
            {
                "id": 3242822893768,
                "name": "#1002",
                "note": "",
                "tags": "",
                "test": True,
                "email": "",
                "phone": None,
                "token": "334ed1552d8c5981a29c7ec2c3c60184",
                "app_id": 1354745,
                "number": 2,
                "gateway": "bogus",
                "refunds": [],
                "user_id": 69761204424,
                "currency": "BRL",
                "customer": {
                    "id": 4651180654792,
                    "note": None,
                    "tags": "",
                    "email": None,
                    "phone": None,
                    "state": "disabled",
                    "currency": "BRL",
                    "last_name": "",
                    "created_at": "2021-02-03T17:11:42-03:00",
                    "first_name": "Teste",
                    "tax_exempt": False,
                    "updated_at": "2021-02-03T17:11:42-03:00",
                    "total_spent": "0.00",
                    "orders_count": 0,
                    "last_order_id": None,
                    "tax_exemptions": [],
                    "verified_email": True,
                    "last_order_name": None,
                    "accepts_marketing": False,
                    "admin_graphql_api_id": "gid://shopify/Customer/4651180654792",
                    "multipass_identifier": None,
                    "marketing_opt_in_level": None,
                    "accepts_marketing_updated_at": "2021-02-03T17:11:42-03:00",
                },
                "closed_at": None,
                "confirmed": True,
                "device_id": None,
                "reference": None,
                "tax_lines": [
                    {
                        "rate": 0.17,
                        "price": "17.85",
                        "title": "VAT",
                        "price_set": {
                            "shop_money": {
                                "amount": "17.85",
                                "currency_code": "BRL",
                            },
                            "presentment_money": {
                                "amount": "17.85",
                                "currency_code": "BRL",
                            },
                        },
                    }
                ],
                "total_tax": "17.85",
                "browser_ip": "179.223.197.72",
                "cart_token": "",
                "created_at": "2021-02-03T17:11:44-03:00",
                "line_items": [
                    {
                        "id": 9210212188360,
                        "sku": "",
                        "name": "Network card",
                        "grams": 0,
                        "price": "105.00",
                        "title": "Network card",
                        "duties": [],
                        "vendor": "meyadev",
                        "taxable": True,
                        "quantity": 1,
                        "gift_card": False,
                        "price_set": {
                            "shop_money": {
                                "amount": "105.00",
                                "currency_code": "BRL",
                            },
                            "presentment_money": {
                                "amount": "105.00",
                                "currency_code": "BRL",
                            },
                        },
                        "tax_lines": [
                            {
                                "rate": 0.17,
                                "price": "17.85",
                                "title": "VAT",
                                "price_set": {
                                    "shop_money": {
                                        "amount": "17.85",
                                        "currency_code": "BRL",
                                    },
                                    "presentment_money": {
                                        "amount": "17.85",
                                        "currency_code": "BRL",
                                    },
                                },
                            }
                        ],
                        "product_id": 6219191091400,
                        "properties": [],
                        "variant_id": 37975221534920,
                        "variant_title": "",
                        "product_exists": True,
                        "total_discount": "0.00",
                        "origin_location": {
                            "id": 2716531523784,
                            "zip": "89031-004",
                            "city": "Blumenau",
                            "name": "Rua Gustavo Salinger 47",
                            "address1": "Rua Gustavo Salinger 47",
                            "address2": "apartment 1306",
                            "country_code": "BR",
                            "province_code": "SC",
                        },
                        "requires_shipping": True,
                        "fulfillment_status": None,
                        "total_discount_set": {
                            "shop_money": {
                                "amount": "0.00",
                                "currency_code": "BRL",
                            },
                            "presentment_money": {
                                "amount": "0.00",
                                "currency_code": "BRL",
                            },
                        },
                        "fulfillment_service": "manual",
                        "admin_graphql_api_id": "gid://shopify/LineItem/9210212188360",
                        "discount_allocations": [],
                        "fulfillable_quantity": 1,
                        "variant_inventory_management": "shopify",
                    }
                ],
                "source_url": None,
                "updated_at": "2021-02-03T17:11:45-03:00",
                "checkout_id": 19110280036552,
                "location_id": 59759493320,
                "source_name": "shopify_draft_order",
                "total_price": "122.85",
                "cancelled_at": None,
                "fulfillments": [],
                "landing_site": None,
                "order_number": 1002,
                "processed_at": "2021-02-03T17:11:43-03:00",
                "total_weight": 0,
                "cancel_reason": None,
                "contact_email": None,
                "total_tax_set": {
                    "shop_money": {"amount": "17.85", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "17.85",
                        "currency_code": "BRL",
                    },
                },
                "checkout_token": "7f4ec2c3d0c922e576f85cfcade2e7d4",
                "client_details": {
                    "browser_ip": "179.223.197.72",
                    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
                    "session_hash": None,
                    "browser_width": None,
                    "browser_height": None,
                    "accept_language": "en-US,en;q=0.9",
                },
                "discount_codes": [],
                "referring_site": None,
                "shipping_lines": [],
                "subtotal_price": "105.00",
                "taxes_included": False,
                "customer_locale": None,
                "note_attributes": [],
                "payment_details": {
                    "avs_result_code": None,
                    "credit_card_bin": "1",
                    "cvv_result_code": None,
                    "credit_card_number": "•••• •••• •••• 1",
                    "credit_card_company": "Bogus",
                },
                "total_discounts": "0.00",
                "total_price_set": {
                    "shop_money": {"amount": "122.85", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "122.85",
                        "currency_code": "BRL",
                    },
                },
                "total_price_usd": "22.88",
                "financial_status": "paid",
                "landing_site_ref": None,
                "order_status_url": "https://meyadev.myshopify.com/53374124232/orders/334ed1552d8c5981a29c7ec2c3c60184/authenticate?key=a51d5fcf7735bf602c512e64f056d51d",
                "processing_method": "direct",
                "source_identifier": None,
                "fulfillment_status": None,
                "subtotal_price_set": {
                    "shop_money": {"amount": "105.00", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "105.00",
                        "currency_code": "BRL",
                    },
                },
                "total_tip_received": "0.0",
                "total_discounts_set": {
                    "shop_money": {"amount": "0.00", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "0.00",
                        "currency_code": "BRL",
                    },
                },
                "admin_graphql_api_id": "gid://shopify/Order/3242822893768",
                "presentment_currency": "BRL",
                "discount_applications": [],
                "payment_gateway_names": ["bogus"],
                "total_line_items_price": "105.00",
                "buyer_accepts_marketing": False,
                "current_total_duties_set": None,
                "total_shipping_price_set": {
                    "shop_money": {"amount": "0.00", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "0.00",
                        "currency_code": "BRL",
                    },
                },
                "original_total_duties_set": None,
                "total_line_items_price_set": {
                    "shop_money": {"amount": "105.00", "currency_code": "BRL"},
                    "presentment_money": {
                        "amount": "105.00",
                        "currency_code": "BRL",
                    },
                },
            }
        )

        assert True
    except Exception as e:
        print(e)
        assert False
