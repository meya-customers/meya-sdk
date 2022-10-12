from meya.front.payload.payload import FrontPagination
from meya.front.payload.teammate import FrontTeammateGet
from meya.front.payload.teammate import FrontTeammateList


def test_front_teammate_list():
    assert FrontTeammateList.from_dict(
        {
            "_pagination": {"next": None},
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/teammates"
            },
            "_results": [
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "username": "amanie",
                    "first_name": "Amanie",
                    "last_name": "Ismail",
                    "is_admin": True,
                    "is_available": True,
                    "is_blocked": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/conversations",
                        },
                    },
                    "id": "tea_d0tj",
                    "email": "support@meya.ai",
                    "username": "support",
                    "first_name": "Meya",
                    "last_name": "Bot",
                    "is_admin": True,
                    "is_available": True,
                    "is_blocked": False,
                    "custom_fields": {},
                },
            ],
        }
    ) == FrontTeammateList(
        pagination=FrontPagination(next=None),
        results=[
            FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                username="amanie",
                first_name="Amanie",
                last_name="Ismail",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
            FrontTeammateGet(
                id="tea_d0tj",
                email="support@meya.ai",
                username="support",
                first_name="Meya",
                last_name="Bot",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
        ],
    )
