from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.trigger.element import Trigger
from typing import List
from typing import Type
from typing import Union


@dataclass
class FlowSetComponent(Component):
    """
    Set flow-scope data.
    """

    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    flow_set: Union[str, dict] = element_field(
        signature=True, meta_name="data"
    )

    async def start(self) -> List[Entry]:
        data = {}
        if isinstance(self.flow_set, str):
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    f'Could not set flow scope property "{self.flow_set}"'
                    f" because flow.result is not set"
                )
            data = {self.flow_set: self.entry.data.get(Trigger.RESULT_KEY)}
        elif isinstance(self.flow_set, dict):
            data = self.flow_set
        return self.respond(data=data)
