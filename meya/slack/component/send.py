from dataclasses import dataclass
from http import HTTPStatus
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from meya.slack.integration import SlackIntegration
from meya.slack.integration import SlackIntegrationRef
from meya.slack.integration.api import SlackApi
from typing import List
from typing import Optional


@dataclass
class SlackSendComponentResponse(ApiComponentResponse):
    result: str = response_field(sensitive=True)


@dataclass
class SlackSendComponent(BaseApiComponent):
    """
    Send a message via Slack.

    Learn more: https://api.slack.com/messaging/webhooks
    Reference: Layout block: https://api.slack.com/reference/block-kit/blocks
    """

    text: Optional[str] = element_field(default=None)
    blocks: Optional[List[dict]] = element_field(default=None)
    wait_for_response: bool = element_field(default=True)
    integration: SlackIntegrationRef = element_field()

    def validate(self):
        super().validate()
        if not (self.text or self.blocks):
            raise self.validation_error(
                "`text` or `blocks` are required for sending using Slack."
            )

    async def start(self) -> List[Entry]:
        integration: SlackIntegration = await self.resolve(self.integration)
        req, res = await SlackApi(webhook_url=integration.webhook_url).send(
            text=self.text,
            blocks=self.blocks,
            wait_for_response=self.wait_for_response,
        )

        if res:
            entries = []
            response = SlackSendComponentResponse(
                status=res.status,
                result=res.text,
                ok=res.status == HTTPStatus.OK,
            )
        else:
            entries = [req]
            response = {}

        return self.respond(*entries, data=response)
