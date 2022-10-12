from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.text.ignorecase import IgnorecaseMixin
from meya.trigger.element import Trigger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class CaseComponent(Component, IgnorecaseMixin):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    value: Any = element_field(default=None)
    ignorecase: Optional[bool] = element_field(default=None)
    case: Dict[Any, ActionComponentSpec] = element_field(signature=True)
    default: ActionComponentSpec = element_field()

    async def start(self) -> List[Entry]:
        if self.value is None:
            # TODO use MISSING_FACTORY instead of None
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    "Case could not be evaluated because flow.result is "
                    "not set"
                )
            value = self.entry.data.get(Trigger.RESULT_KEY)
        else:
            value = self.value

        if self.ignorecase_default_true and isinstance(value, str):
            value = value.lower()

        for case_value, case_action in self.case.items():
            if self.ignorecase_default_true and isinstance(case_value, str):
                case_value = case_value.lower()

            if case_value == value:
                return self.flow_control_action(case_action)

        return self.flow_control_action(self.default)
