from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.trigger.element import Trigger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class MatchComponentResponse:
    result: Any = response_field()
    groups: dict = response_field()
    ok: bool = response_field()


@dataclass
class MatchComponent(Component, IgnorecaseMixin):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    value: Any = element_field(default=None)
    ignorecase: Optional[bool] = element_field(default=None)
    match: Dict[str, ActionComponentSpec] = element_field(signature=True)
    default: ActionComponentSpec = element_field()

    async def start(self) -> List[Entry]:
        if self.value is None:
            # TODO use MISSING_FACTORY instead of None
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    "Match could not be evaluated because flow.result is "
                    "not set"
                )
            value = self.entry.data.get(Trigger.RESULT_KEY)
        else:
            value = self.value
        best_length = -1
        best_action = self.default
        best_response = MatchComponentResponse(
            result=value, groups={}, ok=False
        )
        for match_regex, match_action in self.match.items():
            match = RegexTrigger.search_regex(
                match_regex, value, self.ignorecase_default_true
            )
            if match:
                match_result, match_groups = match
                length = len(match_result)
                if length > best_length:
                    best_length = length
                    best_action = match_action
                    best_response = MatchComponentResponse(
                        result=match_result, groups=match_groups, ok=True
                    )
        return self.flow_control_action(best_action, best_response)
