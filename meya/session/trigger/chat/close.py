from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.session.event.chat.close import ChatCloseEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class ChatCloseTrigger(Trigger):
    extra_alias: str = meta_field(value="chat_close")

    entry: ChatCloseEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        return self.succeed()
