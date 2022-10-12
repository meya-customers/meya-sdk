from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import meta_field
from meya.entry import Entry
from meya.text.event.say import SayEvent
from meya.text.trigger import TextTrigger
from typing import List


@dataclass
class EchoComponent(Component):
    extra_alias: str = meta_field(value="echo")

    async def start(self) -> List[Entry]:
        text = self.entry.data[TextTrigger.RESULT_KEY]
        text_event = SayEvent(text=text)
        return self.respond(text_event)
