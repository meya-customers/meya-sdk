from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import meta_field
from meya.entry import Entry
from meya.orb.event.screen.end import ScreenEndEvent
from typing import List


@dataclass
class ScreenEndComponent(Component):
    extra_alias: str = meta_field(value="end_screen")

    async def start(self) -> List[Entry]:
        open_chat_event = ScreenEndEvent()
        return self.respond(open_chat_event)
