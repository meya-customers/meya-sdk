from dataclasses import dataclass
from meya.bot.element import BotRef
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.meta_tag import ActionComponentTag
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
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
class FlowComponent(Component):
    """
    Start a sub-flow.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/52-arrows-diagrams/02-diagrams/diagram-curve-up-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[BotFlowTag, ActionComponentTag]
    )

    flow: FlowRef = element_field(signature=True)
    jump: Optional[StepLabelRef] = element_field(default=None)
    data: Optional[dict] = element_field(default=None)
    transfer: bool = element_field(default=False)
    async_: bool = element_field(default=False)
    bot: Optional[BotRef] = element_field(default=None)
    thread_id: Optional[str] = element_field(default=None)

    def validate(self):
        super().validate()
        if self.transfer and self.async_:
            raise self.validation_error("transfer is invalid for async flows")
        if self.bot and not self.async_:
            raise self.validation_error("bot is only valid for async flows")
        if self.thread_id and not self.async_:
            raise self.validation_error(
                "thread_id is only valid for async flows"
            )

    async def start(self) -> List[Entry]:
        if self.async_:
            assert self.entry.flow is not None
            return self.flow_control_start_async(
                flow=self.flow,
                label=self.jump,
                data=self.data,
                bot=self.bot,
                thread_id=self.thread_id,
            )
        elif self.transfer:
            assert self.entry.flow is not None
            return self.flow_control_jump_start(
                flow=self.flow, label=self.jump, data=self.data
            )
        else:
            # TODO: Remove redundant "parent_flow" once empty data dict schema is fixed
            return self.flow_control_start(
                flow=self.flow, label=self.jump, data=self.data
            )
