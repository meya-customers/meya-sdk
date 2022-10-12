from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import meta_field
from meya.entry import Entry
from meya.orb.event.screen.continue_ import ScreenContinueEvent
from typing import List
from typing import Optional


@dataclass
class ScreenContinueComponent(Component):
    extra_alias: str = meta_field(value="continue_screen")

    async def start(self) -> List[Entry]:
        open_chat_event = ScreenContinueEvent()
        return self.respond(open_chat_event)
