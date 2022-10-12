from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.meta_tag import ActionComponentTag
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import context_field
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.icon.spec import IconElementSpecUnion
from typing import List
from typing import Optional
from typing import Type


@dataclass
class JumpComponent(Component):
    """
    Jump to another point in the current flow.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/50-navigate/navigation-next.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[BotFlowTag, ActionComponentTag]
    )

    jump: StepLabelRef = element_field(signature=True)
    data: Optional[dict] = element_field(default=None)

    context_flow: FlowRef = context_field()

    async def start(self) -> List[Entry]:
        assert self.entry.flow is not None
        return self.flow_control_jump(label=self.jump, data=self.data)
