from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.entry import Entry
from meya.lifecycle.event.event import LifecycleEvent
from typing import List
from typing import Optional


@dataclass
class LifecycleComponent(Component):
    lifecycle: Optional[str] = element_field(signature=True)
    text: Optional[str] = element_field(default=None)

    async def start(self) -> List[Entry]:
        event = LifecycleEvent(lifecycle_id=self.lifecycle, text=self.text)
        return self.respond(event)
