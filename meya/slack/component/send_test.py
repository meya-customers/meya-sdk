import pytest

from http import HTTPStatus
from meya.db.view.db_test import MockDbView
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_mock_http_response
from meya.element.element_test import verify_process_element
from meya.slack.component.send import SlackSendComponent
from meya.slack.integration import SlackIntegration
from meya.slack.integration import SlackIntegrationRef
from meya.util.dict import to_dict
from typing import List
from typing import Optional


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "text",
        "blocks",
        "wait_for_response",
        "response_status",
        "response_text",
    ),
    [("This is text", None, True, HTTPStatus.OK, "ok")],
)
async def test_slack_send_component(
    text: Optional[str],
    blocks: Optional[List[dict]],
    wait_for_response: bool,
    response_status: int,
    response_text: str,
):
    integration_ref = SlackIntegrationRef(ref="integration.slack")
    integration_element = SlackIntegration(
        id=integration_ref.ref,
        webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    )

    kwargs = dict(
        integration=integration_ref, wait_for_response=wait_for_response
    )
    if text:
        kwargs["text"] = text
    if blocks:
        kwargs["blocks"] = blocks

    component = SlackSendComponent(**kwargs)
    component_start_entry = create_component_start_entry(component)
    http_mock = create_mock_http_response(
        status=response_status, text=response_text
    )
    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(
            result=to_dict(
                await MockDbView().encrypt_sensitive(response_text)
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
