from dataclasses import dataclass
from http import HTTPStatus
from meya.calendly.integration import CalendlyIntegration
from meya.calendly.integration import CalendlyIntegrationRef
from meya.calendly.integration.api import CalendlyApi
from meya.calendly.payload.payload import CalendlyEventType
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from typing import List


@dataclass
class CalendlyCreateWebhookComponent(BaseApiComponent):
    """
    Learn more: https://developer.calendly.com/docs/webhook-subscriptions
    """

    url: str = element_field(default=None)
    events: List[CalendlyEventType] = element_field(
        default_factory=CalendlyEventType.all
    )
    wait_for_response: bool = element_field(default=True)
    integration: CalendlyIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: CalendlyIntegration = await self.resolve(self.integration)
        if not self.url:
            self.url = integration.gateway_webhook_url

        req, res = await integration.api.subscribe(
            url=self.url,
            events=self.events,
            wait_for_response=self.wait_for_response,
        )
        if res:
            entries = []
            response = ApiComponentResponse(
                status=res.status,
                result=res.data,
                ok=res.status == HTTPStatus.CREATED,
            )
        else:
            entries = [req]
            response = {}

        return self.respond(*entries, data=response)
