from dataclasses import dataclass
from meya.analytics.event.track import TrackEvent
from meya.component.element import Component
from meya.element.field import element_field
from meya.entry import Entry
from numbers import Real
from typing import List
from typing import Optional


@dataclass
class TrackComponent(Component):
    track: str = element_field(signature=True)
    data: Optional[dict] = element_field(default=None)
    timestamp: Optional[Real] = element_field(default=None)

    async def start(self) -> List[Entry]:
        track_event = TrackEvent(
            event=self.track,
            data=self.data,
            context=self.context,
            timestamp=self.timestamp,
        )
        return self.respond(track_event)
