from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.text.event.status import StatusEvent
from typing import List


@dataclass
class StatusComponent(InteractiveComponent):
    status: str = element_field(signature=True)
    ephemeral: bool = element_field(default=False)

    async def start(self) -> List[Entry]:
        status_event = StatusEvent(
            status=self.status, ephemeral=self.ephemeral
        )
        return self.respond(status_event)
