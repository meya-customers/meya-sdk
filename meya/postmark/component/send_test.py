import pytest

from http import HTTPStatus
from meya.db.view.db_test import MockDbView
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_mock_http_response
from meya.element.element_test import verify_process_element
from meya.email import Recipient
from meya.postmark.component.send import PostmarkSendComponent
from meya.postmark.integration import PostmarkIntegration
from meya.postmark.integration import PostmarkIntegrationRef
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
                "To": "Inigo Montoya <erik+inigo@meya.ai>",
                "SubmittedAt": "2020-05-19T21:56:44.9569049-04:00",
                "MessageID": "7ddbbb41-05df-4401-beae-3264d4bd6ca5",
                "ErrorCode": 0,
                "Message": "OK",
            },
        )
    ],
)
async def test_postmark_send_component(
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
    integration_ref = PostmarkIntegrationRef(ref="integration.postmark")
    integration_element = PostmarkIntegration(
        id=integration_ref.ref, server_token="server_token_here"
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

    component = PostmarkSendComponent(**kwargs)
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
