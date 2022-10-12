from meya.front.payload.contact import FrontContactCreateHandle
from meya.front.payload.contact import FrontContactCreateLinks
from meya.front.payload.contact import FrontContactCreateRelated
from meya.front.payload.contact import FrontContactCreateResponse
from meya.front.payload.contact import FrontSource


def test_front_contact_response_payload():
    assert FrontContactCreateResponse(
        id="crd_1qmsnpj",
        description="",
        links=FrontContactCreateLinks(
            related=FrontContactCreateRelated(
                notes="https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qmsnpj/notes",
                conversations="https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qmsnpj/conversations",
            )
        ),
        updated_at=1623110769.31,
        is_private=False,
        name=None,
        avatar_url=None,
        groups=[],
        handles=[
            FrontContactCreateHandle(source=FrontSource.CUSTOM, handle="test")
        ],
        custom_fields={},
    ) == FrontContactCreateResponse.from_dict(
        {
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qmsnpj",
                "related": {
                    "notes": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qmsnpj/notes",
                    "conversations": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qmsnpj/conversations",
                    "owner": None,
                },
            },
            "id": "crd_1qmsnpj",
            "name": None,
            "description": "",
            "avatar_url": None,
            "links": [],
            "handles": [{"source": "custom", "handle": "test"}],
            "groups": [],
            "updated_at": 1623110769.31,
            "custom_fields": {},
            "is_private": False,
        }
    )
