import random

from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from typing import List
from typing import Type


@dataclass
class RandomComponent(Component):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    random: List[ActionComponentSpec] = element_field(signature=True)

    async def start(self) -> List[Entry]:
        return self.flow_control_action(random.choice(self.random))
