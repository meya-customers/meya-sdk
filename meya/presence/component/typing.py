from dataclasses import dataclass
from enum import Enum
from meya.component.element import Component
from meya.element.field import element_field
from meya.entry import Entry
from meya.presence.event.typing.off import TypingOffEvent
from meya.presence.event.typing.on import TypingOnEvent
from typing import List


class TypingState(Enum):
    ON = "on"
    OFF = "off"


@dataclass
class TypingComponent(Component):
    typing: TypingState = element_field(signature=True)

    async def start(self) -> List[Entry]:
        if self.typing == TypingState.ON:
            return self.respond(TypingOnEvent())
        else:
            return self.respond(TypingOffEvent())
