from dataclasses import dataclass
from meya.button.event.click import ButtonClickEvent
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class ButtonTrigger(Trigger):
    @dataclass
    class Response:
        context: Dict[str, Any] = response_field()

    button_id: str = element_field(signature=True)
    text: Optional[str] = element_field(default=None)
    when: Any = element_field(default=True)

    entry: ButtonClickEvent = process_field()
    encrypted_entry: ButtonClickEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        if self.button_id != self.entry.button_id:
            return self.fail()
        else:
            return self.succeed(
                data=ButtonTrigger.Response(
                    context=self.encrypted_entry.context
                )
            )
