from dataclasses import dataclass
from http import HTTPStatus
from meya.calendly.integration.api import CalendlyApi
from meya.calendly.payload.payload import CalendlyWebhook
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.element.field import process_field
from meya.entry import Entry
from meya.http.entry.request import HttpRequestEntry
from meya.integration.element import Integration
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type


@dataclass
class CalendlyIntegration(Integration):
    NAME: ClassVar[str] = "calendly"

    api_key: Optional[str] = element_field(default=None)
    access_token: Optional[str] = element_field(default=None)

    entry: HttpRequestEntry = process_field()

    async def rx(self) -> List[Entry]:
        try:
            webhook = CalendlyWebhook.from_dict(self.entry.data)
        except ValueError:
            # invalid webhook data
            # TODO: should we return a 401 instead?
            return self.respond(
                status=HTTPStatus.OK,
                data=dict(ok=False, message="Invalid webhook data."),
            )

        calendly_event = webhook.to_event()
        if calendly_event:
            return self.respond(calendly_event, status=HTTPStatus.OK)

        else:
            # unsupported type
            return self.respond(
                status=HTTPStatus.OK,
                data=dict(ok=False, message="Event not handled."),
            )

    @property
    def api(self) -> CalendlyApi:
        return CalendlyApi(
            api_key=self.api_key, access_token=self.access_token
        )


class CalendlyIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = CalendlyIntegration
