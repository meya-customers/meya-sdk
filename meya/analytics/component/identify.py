from dataclasses import dataclass
from meya.analytics.event.identify import IdentifyEvent
from meya.component.element import Component
from meya.element.field import element_field
from meya.entry import Entry
from numbers import Real
from typing import List
from typing import Optional


@dataclass
class IdentifyComponent(Component):
    identify: dict = element_field(signature=True)
    timestamp: Optional[Real] = element_field(default=None)

    async def start(self) -> List[Entry]:
        identify_event = IdentifyEvent(
            data=self.identify, context=self.context, timestamp=self.timestamp
        )
        return self.respond(identify_event)
