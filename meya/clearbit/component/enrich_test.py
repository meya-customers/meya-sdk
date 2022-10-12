import pytest

from http import HTTPStatus
from meya.clearbit.component.enrich import ClearbitEnrichComponent
from meya.clearbit.integration import ClearbitIntegration
from meya.clearbit.integration import ClearbitIntegrationRef
from meya.clearbit.integration.api import ClearbitEnrichedEmail
from meya.db.view.db_test import MockDbView
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_mock_http_response
from meya.element.element_test import verify_process_element
from meya.util.dict import to_dict

CLEARBIT_API_KEY = "sk_e6fd932cf5850b44819f09b2edf23412"
CLEARBIT_PERSON = {
    "id": "d54c54ad-40be-4305-8a34-0ab44710b90d",
    "name": {
        "fullName": "Alex MacCaw",
        "givenName": "Alex",
        "familyName": "MacCaw",
    },
    "email": "alex@clearbit.com",
    "//": "...",
}
CLEARBIT_COMPANY = {
    "id": "c5a6a9c5-303a-455a-935c-9dffcd2ed756",
    "name": "Clearbit",
    "legalName": "APIHub, Inc",
    "domain": "clearbit.com",
    "//": "...",
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("email", "response_status", "response_data"),
    [
        (
            "alex@clearbit.com",
            HTTPStatus.OK,
            {"person": CLEARBIT_PERSON, "company": CLEARBIT_COMPANY},
        ),
        (
            "notaperson@clearbit.com",
            HTTPStatus.OK,
            {"person": None, "company": CLEARBIT_COMPANY},
        ),
        (
            "alex.mccaw@gmail.com",
            HTTPStatus.OK,
            {"person": CLEARBIT_PERSON, "company": None},
        ),
        (
            "notaperson@notacompany.com",
            HTTPStatus.NOT_FOUND,
            {
                "error": {
                    "type": "unknown_record",
                    "message": "Unknown person.",
                }
            },
        ),
        (
            "asdf",
            HTTPStatus.UNPROCESSABLE_ENTITY,
            {"error": {"type": "email_invalid", "message": "Invalid email."}},
        ),
        (
            "alex@clearbit.com",
            HTTPStatus.TOO_MANY_REQUESTS,
            {
                "error": {
                    "type": "rate_limit",
                    "message": "Rate limit exceeded. Limit is 600 requests per minute. Rate limit will be reset in 50 seconds.",
                }
            },
        ),
    ],
)
async def test_clearbit_enrich_component(
    email: str, response_status: int, response_data: dict
):
    integration_ref = ClearbitIntegrationRef(ref="integration.clearbit")
    integration_element = ClearbitIntegration(
        id=integration_ref.ref, api_key=CLEARBIT_API_KEY
    )
    component = ClearbitEnrichComponent(
        email=email, integration=integration_ref
    )
    component_start_entry = create_component_start_entry(component)
    http_mock = create_mock_http_response(
        status=response_status, data=response_data
    )

    ok = response_status == HTTPStatus.OK
    if ok:
        enriched_email = ClearbitEnrichedEmail(
            **{**dict(email=email), **response_data}
        )
        enriched_email_dict = to_dict(enriched_email)
        data = None

        assert enriched_email.is_enriched == ok
        assert enriched_email.email == email
        if bool(enriched_email.person):
            assert bool(enriched_email.person["name"])
        if bool(enriched_email.company):
            assert bool(enriched_email.company["name"])
    else:
        enriched_email_dict = None
        data = response_data

    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(
            result=enriched_email_dict
            and to_dict(
                await MockDbView().encrypt_sensitive(enriched_email_dict)
            ),
            data=data and to_dict(await MockDbView().encrypt_sensitive(data)),
            status=response_status,
            ok=ok,
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        [flow_next_entry],
        http_mock=http_mock,
        extra_elements=[integration_element],
    )
