from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.text.event.info import InfoEvent
from meya.widget.component import WidgetComponent
from typing import List


@dataclass
class InfoComponent(WidgetComponent):
    info: str = element_field(signature=True)

    async def build(self) -> List[Entry]:
        event = InfoEvent(info=self.info)
        return self.respond(event)
