from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import meta_field
from meya.entry import Entry
from meya.session.event.chat.open import ChatOpenEvent
from typing import List


@dataclass
class ChatOpenComponent(Component):
    extra_alias: str = meta_field(value="open_chat")

    async def start(self) -> List[Entry]:
        open_chat_event = ChatOpenEvent()
        return self.respond(open_chat_event)
