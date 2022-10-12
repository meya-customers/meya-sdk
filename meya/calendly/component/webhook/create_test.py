import pytest

from http import HTTPStatus
from meya.calendly.component.webhook.create import (
    CalendlyCreateWebhookComponent,
)
from meya.calendly.integration import CalendlyIntegration
from meya.calendly.integration import CalendlyIntegrationRef
from meya.calendly.payload.payload import CalendlyEventType
from meya.db.view.db_test import MockDbView
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_mock_http_response
from meya.element.element_test import verify_process_element
from meya.util.dict import to_dict
from typing import List
from typing import Optional


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("url", "events", "response_status", "response_data"),
    [
        (
            "https://www.domain.com/path/to/webhook",
            None,
            HTTPStatus.CREATED,
            {"id": 538107},
        ),
        (
            "https://www.domain.com/path/to/webhook",
            None,
            HTTPStatus.CONFLICT,
            {
                "type": "conflict_error",
                "message": "Hook with this url already exists",
            },
        ),
        (
            "https://www.domain.com/path/to/webhook",
            [CalendlyEventType.INVITEE_CREATED],
            HTTPStatus.CREATED,
            {"id": 538107},
        ),
    ],
)
async def test_create_webhook_start(
    url: str,
    events: Optional[List[CalendlyEventType]],
    response_status: int,
    response_data: dict,
):
    if events is None:
        events = CalendlyEventType.all()
    integration_ref = CalendlyIntegrationRef(ref="integration.calendly")
    integration_element = CalendlyIntegration(
        id=integration_ref.ref, api_key="key123"
    )
    component = CalendlyCreateWebhookComponent(
        integration=integration_ref, url=url, events=events
    )
    component_start_entry = create_component_start_entry(component)
    http_mock = create_mock_http_response(
        status=response_status, data=response_data
    )

    ok = response_status == HTTPStatus.CREATED
    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(
            result=to_dict(
                await MockDbView().encrypt_sensitive(response_data)
            ),
            status=response_status,
            ok=ok,
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        expected_pub_entries=[flow_next_entry],
        http_mock=http_mock,
        extra_elements=[integration_element],
    )
