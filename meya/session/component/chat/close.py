from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import meta_field
from meya.entry import Entry
from meya.session.event.chat.close import ChatCloseEvent
from typing import List


@dataclass
class ChatCloseComponent(Component):
    extra_alias: str = meta_field(value="close_chat")

    async def start(self) -> List[Entry]:
        open_chat_event = ChatCloseEvent()
        return self.respond(open_chat_event)
