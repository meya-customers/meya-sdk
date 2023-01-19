from dataclasses import dataclass
from meya.csp.event.agent.command import AgentCommandEvent
from meya.db.view.user import UserType
from meya.element.field import element_field
from meya.element.field import process_field
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger import TextTrigger
from meya.text.trigger.regex import RegexTrigger
from meya.text.trigger.regex import RegexTriggerResponse
from meya.trigger.element import TriggerMatchResult
from typing import Optional


@dataclass
class AgentCommandTrigger(TextTrigger, IgnorecaseMixin):
    """
    Match the agent command against a regex pattern.

    Meya uses the [Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax).
    """

    agent_command: str = element_field(
        signature=True,
        help=(
            "The regex (regular expression) pattern to match the agent "
            "input against."
        ),
    )
    ignorecase: Optional[bool] = element_field(
        default=None, help="Ignore the case of the agent command."
    )
    entry: AgentCommandEvent = process_field()
    encrypted_entry: AgentCommandEvent = process_field()

    async def default_when(self) -> bool:
        if self.event_user.type != UserType.AGENT:
            return False
        return True

    async def match(self) -> TriggerMatchResult:
        match = RegexTrigger.search_regex(
            self.agent_command, self.entry.text, self.ignorecase_default_true
        )
        if match is not None:
            match_result, match_groups = match
            return self.succeed(
                data=RegexTriggerResponse(
                    result=match_result, groups=match_groups
                )
            )
        else:
            return self.fail()
