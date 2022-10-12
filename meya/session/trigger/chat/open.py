from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.session.event.chat.open import ChatOpenEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class ChatOpenTrigger(Trigger):
    extra_alias: str = meta_field(value="chat_open")

    entry: ChatOpenEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        return self.succeed()
