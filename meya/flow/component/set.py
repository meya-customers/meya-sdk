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
    Set flow scope data.

    ```yaml
    - flow_set:
        some_result: (@ flow.result )
        foo: bar
        a:
          a: 123
          list:
            - item 1
            - item 2
            - b: 123
              c: 123
    ```

    The `flow_set` component takes and arbitrary dictionary of data that can
    contain nested dictionaries, values and lists.

    You can also use [Meya template syntax](https://docs.meya.ai/docs/jinja2-syntax) to render data
    into the flow scope.

    Also check the [Flow scope guide](https://docs.meya.ai/docs/scope#flow).

    ### Implicit `flow.result` reference
    You can also reference the `(@ flow.result )` value when setting a single
    key. This is useful if you do not want to type the extra template syntax
    explicitly.

    For example:
    ```yaml
    steps:
      - ask: What is your name?
      - flow_set: name
    ```

    Is the short form of:

    ```yaml
    steps:
      - ask: What is you name?
      - flow_set:
          name: (@ flow.result )
    ```
    """

    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    flow_set: Union[str, dict] = element_field(
        signature=True,
        meta_name="data",
        help=(
            "This can either be a dictionary of values, or just the name of "
            "a single flow scope variable. If just a name is provided, then "
            "the value in `(@ flow.result )` will be stored under the given "
            "name in the flow data scope."
        ),
    )

    async def start(self) -> List[Entry]:
        data = {}
        if isinstance(self.flow_set, str):
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    f'Could not set flow scope variable "{self.flow_set}"'
                    f" because flow.result is not set"
                )
            data = {self.flow_set: self.entry.data.get(Trigger.RESULT_KEY)}
        elif isinstance(self.flow_set, dict):
            data = self.flow_set
        return self.respond(data=data)
