import pytest

from http import HTTPStatus
from meya.db.view.db_test import MockDbView
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_mock_http_response
from meya.element.element_test import verify_process_element
from meya.email import Recipient
from meya.mailgun.component.send import MailgunSendComponent
from meya.mailgun.integration import MailgunIntegration
from meya.mailgun.integration import MailgunIntegrationRef
from meya.util.dict import to_dict
from typing import List


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "from_",
        "to",
        "cc",
        "bcc",
        "subject",
        "text",
        "html",
        "response_status",
        "response_data",
    ),
    [
        (
            Recipient(email="rx@domain1.com"),
            [Recipient(email="tx@domain2.com")],
            [],
            [],
            "Subject here 123",
            "Text here 456",
            None,
            HTTPStatus.OK,
            {
                "id": "<email123@abc456.mailgun.org>",
                "message": "Queued. Thank you.",
            },
        )
    ],
)
async def test_mailgun_send_component(
    from_: Recipient,
    to: List[Recipient],
    cc: List[Recipient],
    bcc: List[Recipient],
    subject: str,
    text: str,
    html: str,
    response_status: int,
    response_data: dict,
):
    integration_ref = MailgunIntegrationRef(ref="integration.mailgun")
    integration_element = MailgunIntegration(
        id=integration_ref.ref, api_key="api_key_here", domain="domain_here"
    )

    kwargs = dict(
        integration=integration_ref, from_=from_, to=to, cc=cc, bcc=bcc
    )
    if subject:
        kwargs["subject"] = subject
    if text:
        kwargs["text"] = text
    if html:
        kwargs["html"] = html

    component = MailgunSendComponent(**kwargs)
    component_start_entry = create_component_start_entry(component)
    http_mock = create_mock_http_response(
        status=response_status, data=response_data
    )
    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(
            result=to_dict(
                await MockDbView().encrypt_sensitive(response_data)
            ),
            status=response_status,
            ok=response_status == HTTPStatus.OK,
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        [flow_next_entry],
        http_mock=http_mock,
        extra_elements=[integration_element],
    )
