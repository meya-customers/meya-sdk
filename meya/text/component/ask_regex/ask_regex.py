from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.text.component.ask import AskValidationError
from meya.text.component.ask.catchall import AskCatchallComponent
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.text.trigger.regex import RegexTriggerResponse
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from typing import Any
from typing import Optional


@dataclass
class AskRegexComposerComponentOkResponse:
    result: str = response_field(sensitive=True)
    groups: dict = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class AskRegexComponent(AskCatchallComponent, IgnorecaseMixin):
    regex: str = element_field(signature=True)
    ignorecase: Optional[bool] = element_field(default=None)

    def trigger(self, data: Any = None) -> TriggerActivateEntry:
        return RegexTrigger(
            regex=self.regex,
            ignorecase=self.ignorecase,
            confidence=self.confidence,
            action=self.get_next_action(data=data),
        ).activate()

    async def next_response(self) -> Any:
        encrypted_trigger_response = from_dict(
            RegexTriggerResponse, self.entry.data
        )
        match_result = encrypted_trigger_response.result
        match_groups = encrypted_trigger_response.groups

        if self.catchall and not match_result:
            raise AskValidationError()

        return AskRegexComposerComponentOkResponse(
            result=match_result, groups=match_groups
        )
