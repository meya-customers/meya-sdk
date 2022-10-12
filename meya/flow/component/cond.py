from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from typing import Any
from typing import Dict
from typing import List
from typing import Type


@dataclass
class CondComponent(Component):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    cond: List[Dict[Any, ActionComponentSpec]] = element_field(signature=True)
    default: ActionComponentSpec = element_field()

    async def start(self) -> List[Entry]:
        for cond_branch in self.cond:
            cond_items = list(cond_branch.items())
            if len(cond_items) != 1:
                # TODO move this to validate()
                raise self.validation_error(
                    f"Cond expects one key and one value, not {cond_branch}"
                )
            [(cond_value, cond_action)] = cond_items
            if cond_value:
                return self.flow_control_action(cond_action)

        return self.flow_control_action(self.default)
