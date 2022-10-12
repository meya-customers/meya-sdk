import pytest

from meya.calendly.integration import CalendlyIntegration
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyWebhook
from meya.calendly.payload.payload_test import INVITEE_CANCELED_PAYLOAD
from meya.calendly.payload.payload_test import INVITEE_CREATED_PAYLOAD
from meya.calendly.payload.payload_test import ROGUE_EVENT_TYPE
from meya.calendly.payload.payload_test import ROGUE_INVITEE_CREATED
from meya.calendly.payload.payload_test import SAMPLED_INVITEE_CREATED
from meya.calendly.payload.payload_test import STATIC_INVITEE_CREATED
from meya.element.element_test import create_http_request_entry
from meya.element.element_test import create_http_response_entry
from meya.element.element_test import verify_process_element
from typing import Optional


@pytest.mark.parametrize(
    ("data", "event_type", "valid"),
    [
        (INVITEE_CREATED_PAYLOAD, CalendlyEventType.INVITEE_CREATED, True),
        (INVITEE_CANCELED_PAYLOAD, CalendlyEventType.INVITEE_CANCELED, True),
        ({}, None, False),
        (SAMPLED_INVITEE_CREATED, CalendlyEventType.INVITEE_CREATED, True),
        (STATIC_INVITEE_CREATED, CalendlyEventType.INVITEE_CREATED, True),
        (ROGUE_INVITEE_CREATED, CalendlyEventType.INVITEE_CREATED, False),
        (ROGUE_EVENT_TYPE, None, False),
    ],
)
@pytest.mark.asyncio
async def test_calendly_rx(
    data: dict, event_type: Optional[CalendlyEventType], valid: bool
):
    integration = CalendlyIntegration(id="integration.calendly", api_key="xx")
    request_entry = create_http_request_entry(
        integration, data=data, headers={"X-Calendly-Hook-Id": "519639"}
    )
    pub_entries = []
    if valid:
        webhook = CalendlyWebhook.from_dict(data)
        webhook_event = webhook.to_event()
        webhook_event.integration_id = integration.id
        pub_entries.append(webhook_event)
        pub_entries.append(create_http_response_entry(request_entry))
    elif event_type is None:
        pub_entries.append(
            create_http_response_entry(
                request_entry,
                data=dict(ok=False, message="Invalid webhook data."),
            )
        )
    else:
        pub_entries.append(
            create_http_response_entry(
                request_entry,
                data=dict(ok=False, message="Event not handled."),
            )
        )

    await verify_process_element(
        element=integration,
        sub_entry=request_entry,
        expected_pub_entries=pub_entries,
    )
