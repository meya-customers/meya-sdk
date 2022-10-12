from dataclasses import dataclass
from meya.component.element import Component
from meya.csp.event.monitor import MonitorEvent
from meya.csp.integration import CspIntegrationRef
from meya.element.field import element_field
from meya.entry import Entry
from typing import List
from typing import Optional


@dataclass
class MonitorComponent(Component):
    integration: CspIntegrationRef = element_field()
    note: Optional[str] = element_field(default=None)
    data: Optional[dict] = element_field(default=None)

    async def start(self) -> List[Entry]:
        track_event = MonitorEvent(
            data=self.data,
            csp_integration_id=self.integration.ref,
            note=self.note,
        )
        return self.respond(track_event)
