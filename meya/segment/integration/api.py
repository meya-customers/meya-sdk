from dataclasses import dataclass
from datetime import datetime
from meya.db.view.http import HttpBasicAuth
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.segment.payload.payload import IdentifyEvent
from meya.segment.payload.payload import TrackEvent
from meya.util.dict import to_dict
from typing import Optional

API_ROOT = "https://api.segment.io/v1"


def timestamp_to_ISO8601(timestamp: float) -> str:
    return datetime.utcfromtimestamp(timestamp).isoformat() + "Z"


@dataclass
class SegmentApi(Api):
    write_key: str
    api_root: str = API_ROOT

    async def track(
        self, track_event: TrackEvent, wait_for_response: bool = True
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        req = self.http.make_request_entry(
            "POST",
            url=f"{self.api_root}/track",
            json=to_dict(track_event),
            auth=self.auth,
        )
        return (req, await self.http.send(req) if wait_for_response else None)

    async def identify(
        self, identify_event: IdentifyEvent, wait_for_response: bool = True
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        req = self.http.make_request_entry(
            "POST",
            url=f"{self.api_root}/identify",
            json=to_dict(identify_event),
            auth=self.auth,
        )
        return (req, await self.http.send(req) if wait_for_response else None)

    @property
    def auth(self):
        return HttpBasicAuth(self.write_key, "")
