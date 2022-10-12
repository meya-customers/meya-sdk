from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.meta_tag import ActionComponentTag
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from typing import List
from typing import Optional
from typing import Type


@dataclass
class EndComponent(Component):
    """
    End the current flow, optionally returning data.
    """

    extra_alias: str = meta_field(value="end")
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/15-video-movies-tv/06-controls/controls-stop.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[BotFlowTag, ActionComponentTag]
    )

    end: Optional[dict] = element_field(
        signature=True, default=None, meta_name="data"
    )

    async def start(self) -> List[Entry]:
        return self.flow_control_end(data=self.end)
