from dataclasses import dataclass
from http import HTTPStatus
from meya.clearbit.integration import ClearbitIntegration
from meya.clearbit.integration import ClearbitIntegrationRef
from meya.clearbit.integration.api import ClearbitApi
from meya.clearbit.integration.api import ClearbitEnrichedEmail
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element.api import ApiComponentResponse
from typing import List
from typing import Optional


@dataclass
class ClearbitEnrichComponentResponse(ApiComponentResponse):
    result: Optional[ClearbitEnrichedEmail] = response_field(
        default=None, sensitive=True
    )
    data: Optional[dict] = response_field(default=None, sensitive=True)


@dataclass
class ClearbitEnrichComponent(BaseApiComponent):
    """
    Enrich an email address using insights from Clearbit.

    Learn more: https://clearbit.com/docs?shell#enrichment-api
    """

    email: str = element_field()
    integration: ClearbitIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: ClearbitIntegration = await self.resolve(self.integration)
        response = await ClearbitApi(api_key=integration.api_key).enrich(
            email=self.email
        )

        enriched_email = None
        if response.status == HTTPStatus.OK:
            try:
                enriched_email = ClearbitEnrichedEmail(
                    **{**dict(email=self.email), **response.data}
                )
            except ValueError:
                pass

        # include response data if enrichment failed
        if enriched_email:
            data = None
            ok = enriched_email.is_enriched
        else:
            data = response.data
            ok = False

        return self.respond(
            data=ClearbitEnrichComponentResponse(
                result=enriched_email, data=data, status=response.status, ok=ok
            )
        )
