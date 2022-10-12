from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from typing import Any
from typing import List
from typing import Type


@dataclass
class IfComponent(Component):
    """
    Conditionally execute one action or another.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/42-multimedia-controls/button-split.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])
    snippet_default: str = meta_field(
        value="""
            if: (@ flow.result )
            then: next
            else: next
        """
    )

    if_: Any = element_field(signature=True, help="Condition to evaluate")
    then: ActionComponentSpec = element_field(
        help="Action executed if condition passes"
    )
    else_: ActionComponentSpec = element_field(
        help="Action executed if condition fails"
    )

    async def start(self) -> List[Entry]:
        if self.if_:
            return self.flow_control_action(self.then)
        else:
            return self.flow_control_action(self.else_)
