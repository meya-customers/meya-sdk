from dataclasses import dataclass
from meya.analytics.integration import AnalyticsIntegration
from meya.element.field import element_field
from meya.http.entry.request import HttpRequestEntry
from meya.segment.integration.api import SegmentApi
from meya.segment.integration.api import timestamp_to_ISO8601
from meya.segment.payload.payload import IdentifyEvent
from meya.segment.payload.payload import TrackEvent
from typing import ClassVar


@dataclass
class SegmentIntegration(AnalyticsIntegration):
    NAME: ClassVar[str] = "segment"
    write_key: str = element_field()

    async def track(self) -> HttpRequestEntry:
        req, _ = await self.api.track(
            track_event=TrackEvent(
                userId=self.user_id,
                event=self.entry_type,
                properties=self.entry_data,
                timestamp=timestamp_to_ISO8601(self.entry_timestamp),
                context=self.entry_context,
            ),
            wait_for_response=False,
        )
        return req

    async def identify(self) -> HttpRequestEntry:
        req, _ = await self.api.identify(
            identify_event=IdentifyEvent(
                userId=self.user_id,
                traits=self.entry_data,
                timestamp=timestamp_to_ISO8601(self.entry_timestamp),
                context=self.entry_context,
            ),
            wait_for_response=False,
        )
        return req

    @property
    def api(self) -> SegmentApi:
        return SegmentApi(write_key=self.write_key)
