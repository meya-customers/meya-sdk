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
    Jump to specific label step in the current flow.

    A **label step** has a special syntax as follows:

    ```yaml
    - (label name)
    ```

    You can then reference these label steps in your jump components:

    ```yaml
    - jump: some_label
    ```

    Here is a complete example:

    ```yaml
    steps:
      - say: Hi
      - jump: second_label

      - (first_label)
      - say: You reached `first_label`
      - end

      - (second_label)
      - say: You reached `second_label`
      - end
    ```

    In this example the flow will jump from the second step to the step
    containing the `second_label` label step, and continue executing the flow
    from there.

    ### Actions

    The `jump` component is commonly used in **action fields** that are present
    in triggers and flow control components.

    For example, here is a flow with a trigger than jumps to a specific label
    step when matched:

    ```yaml
    triggers:
      - keyword: hi
      - keyword: test
        action:
            jump: debug
    steps:
      - say: Hi
      - end

      - (debug)
      - say: Debug message.
    ```

    In this case, when the user types `test`, the `jump` component will execute
    and jump to the `debug` label.

    Here is an example of using a jump component in the `if` component:

    ```yaml
    steps:
      - ask: What is your age?
      - user_set:
          age: (@ flow.result | int )

      - if: (@ user.age > 18 )
        then:
          jump: confirm_age
        else: next
      ...
    ```
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/50-navigate/navigation-next.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[BotFlowTag, ActionComponentTag]
    )

    jump: StepLabelRef = element_field(
        signature=True,
        help="The label to jump to.",
    )
    data: Optional[dict] = element_field(
        default=None,
        help="Flow scope data to set before jumping to the label.",
    )

    context_flow: FlowRef = context_field()

    async def start(self) -> List[Entry]:
        assert self.entry.flow is not None
        return self.flow_control_jump(label=self.jump, data=self.data)
