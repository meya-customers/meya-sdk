from dataclasses import dataclass
from meya.component.element import ComponentOkResponse
from meya.element.field import element_field
from meya.email.trigger.address import EmailAddressTrigger
from meya.email.trigger.address import EmailAddressTriggerResponse
from meya.text.component.ask import AskValidationError
from meya.text.component.ask.catchall import AskCatchallComponent
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from meya.util.enum import SimpleEnum
from typing import Any
from typing import Optional


class Expect(SimpleEnum):
    EMAIL_ADDRESS = "email_address"


@dataclass
class EmailAddressAskComponent(AskCatchallComponent):
    expect: Optional[Expect] = element_field(signature=True, default=None)

    def trigger(self, data: Any = None) -> TriggerActivateEntry:
        return EmailAddressTrigger(
            confidence=self.confidence, action=self.get_next_action(data=data)
        ).activate()

    async def next_response(self) -> Any:
        encrypted_trigger_response = from_dict(
            EmailAddressTriggerResponse, self.entry.data
        )
        if self.catchall and not encrypted_trigger_response.result:
            raise AskValidationError()
        return ComponentOkResponse(result=encrypted_trigger_response.result)
