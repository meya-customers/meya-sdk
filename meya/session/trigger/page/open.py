from dataclasses import dataclass
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserType
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.session.event.page.open import PageOpenEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class PageOpenTrigger(Trigger):
    @dataclass
    class Response:
        result: str = response_field()
        context: Dict[str, Any] = response_field()

    extra_alias: str = meta_field(value="page_open")

    magic_link_error: Optional[bool] = element_field(default=None)

    entry: PageOpenEvent = process_field()
    encrypted_entry: PageOpenEvent = process_field()

    async def default_when(self) -> bool:
        if self.event_user.type != UserType.USER:
            return False
        if self.thread.mode == ThreadMode.BOT:
            return True
        else:
            return False

    async def match(self) -> TriggerMatchResult:
        if (
            self.magic_link_error is True
            and self.entry.magic_link_ok is not False
        ):
            return self.fail()
        elif (
            self.magic_link_error is False
            and self.entry.magic_link_ok is False
        ):
            return self.fail()
        else:
            return self.succeed(
                data=PageOpenTrigger.Response(
                    result=self.encrypted_entry.url,
                    context=self.encrypted_entry.context,
                )
            )
