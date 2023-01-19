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
    """
    Randomly select and execute a component from the list of component
    references set in the `random` field.

    This component uses the standard Python `random.choice` function that
    uses a uniform random distribution to select a choice.

    ```yaml
    - random:
      - say: Option 1
      - say: Option 2
      - say: Option 3
      - flow: flow.some_flow
        transfer: true
      - say: Option 4
    ```

    Each item in the `random` field must contain a valid **action field**,
    meaning the field takes an action spec which maps to the [`ActionComponentSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/component/spec.py)
    Python class. This allows you to execute any component.
    """

    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    random: List[ActionComponentSpec] = element_field(
        signature=True,
        help="A list of component references to randomly select from.",
    )

    async def start(self) -> List[Entry]:
        return self.flow_control_action(random.choice(self.random))
