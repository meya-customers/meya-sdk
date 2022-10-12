from dataclasses import dataclass
from http import HTTPStatus
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyEventV2
from meya.calendly.payload.payload import CalendlyGetEventResponse
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.util.dict import from_dict
from typing import List
from typing import Optional

API_ROOT = "https://calendly.com/api/v1"
API_ROOT_V2 = "https://api.calendly.com"


@dataclass
class CalendlyApi(Api):
    api_key: Optional[str] = None
    access_token: Optional[str] = None
    api_root: str = API_ROOT
    api_root_v2: str = API_ROOT_V2

    async def subscribe(
        self,
        url: str,
        events: List[CalendlyEventType],
        wait_for_response: bool = True,
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        data = dict(url=url, events=[event.value for event in events])

        req = self.http.make_request_entry(
            method="POST",
            url=f"{self.api_root}/hooks",
            json=data,
            headers=self.auth_header,
        )

        if wait_for_response:
            return req, await self.http.send(req)
        else:
            return req, None

    async def get_event(self, calendly_event_id: str) -> CalendlyEventV2:
        response = await self.http.get(
            url=f"{self.api_root_v2}/scheduled_events/{calendly_event_id}",
            headers=self.auth_header_v2,
        )
        response.check_status(HTTPStatus.OK)
        return from_dict(CalendlyGetEventResponse, response.data).resource

    @property
    def auth_header(self) -> dict:
        return {"X-TOKEN": self.api_key.strip()}

    @property
    def auth_header_v2(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}
