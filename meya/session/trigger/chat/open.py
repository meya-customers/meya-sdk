from dataclasses import dataclass
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserType
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.session.event.chat.open import ChatOpenEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class ChatOpenTrigger(Trigger):
    extra_alias: str = meta_field(value="chat_open")

    entry: ChatOpenEvent = process_field()

    async def default_when(self) -> bool:
        if self.event_user.type != UserType.USER:
            return False
        if self.thread.mode == ThreadMode.BOT:
            return True
        else:
            return False

    async def match(self) -> TriggerMatchResult:
        return self.succeed()
