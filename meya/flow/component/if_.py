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
    Conditionally execute one action or another. The if component is the most
    common component used for branching a flow (this is very similar to an
    **if** statement in a convention programming language like Python).

    ```yaml
    - if: (@ user.age > 18 )
      then: next
      else:
        flow: flow.confirm_age
    ```

    In this example the component is checking if the user's age above 18, and
    if so, then it will proceed to the next step, otherwise it will call a
    nested flow named `flow.confirm_age` (check the [nested flows guide](https://docs.meya.ai/docs/flows#nested-flows) for
    more detail on how nested flows work).

    ### Evaluation criteria
    The `if` field contains the evaluation criteria which needs to evaluate to
    either `true` or `false`. For example, we can set the value to `true` which
    will result in the `then` component always being run:

    ```yaml
    - if: true
      then: next
      else: end
    ```

    Conversely, when the `if` field is set to `false`, the `else` component
    will always be run.

    Setting `if` to either `true/false` is not very useful, but when we use the
    [Meya template syntax](https://docs.meya.ai/docs/jinja2-syntax), we can
    create complex evaluation criteria using a combination of [template operators](https://docs.meya.ai/docs/jinja2-syntax#operators)
    and flow/thread/user scope variables.

    ### `then/else` components
    Both the `then` and `else` fields are **action fields**, meaning the field
    takes an action spec which maps to the [`ActionComponentSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/component/spec.py)
    Python class. This allows you to define and execute any component, but
    mostly you will use one of the flow control components such as:

    - [flow](https://docs.meya.ai/reference/meya-flow-component)
    - [flow.next](https://docs.meya.ai/reference/meya-flow-component-next)
    - [flow.end](https://docs.meya.ai/reference/meya-flow-component-end)
    - [flow.jump](https://docs.meya.ai/reference/meya-flow-component-jump)
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

    if_: Any = element_field(
        signature=True,
        help=(
            "Contains the evaluation criteria which is expressed using "
            "Meya's [template syntax](doc:jinja2-syntax)."
        ),
    )
    then: ActionComponentSpec = element_field(
        help=(
            "Contains the action component reference that is called when the "
            "evaluation criteria is `True`."
        )
    )
    else_: ActionComponentSpec = element_field(
        help=(
            "Contains the action component reference that is called when the "
            "evaluation criteria is `False`."
        )
    )

    async def start(self) -> List[Entry]:
        if self.if_:
            return self.flow_control_action(self.then)
        else:
            return self.flow_control_action(self.else_)
