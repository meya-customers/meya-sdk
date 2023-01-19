from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from typing import Any
from typing import Dict
from typing import List
from typing import Type


@dataclass
class CondComponent(Component):
    """
    Specify multiple evaluation criteria and run an action if the criteria
    evaluates to `true`.

    ```yaml
    - cond:
       - (@ user.age < 18):
           flow: flow.confirm_age
       - (@ user.age >= 18 and user.age < 65 ):
           jump: next
       - (@ user.age >= 65):
           flow: flow.retired
      default: next
    ```

    Similar to the [`flow.if`](https://docs.meya.ai/reference/meya-flow-component-if) component's
    `if` field, the evaluation criteria must evaluate to either `true`
    or `false`, and thus we can use [Meya template syntax](https://docs.meya.ai/docs/jinja2-syntax) to
    create complex evaluation criteria using a combination of [template operators](https://docs.meya.ai/docs/jinja2-syntax#operators)
    and flow/thread/user scope variables.

    Also, each condition in the `cond` field must contain a valid **action field**,
    meaning the field takes an action spec which maps to the [`ActionComponentSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/component/spec.py)
    Python class. This allows you to execute any component, but you will mostly
    use one of the flow control components.
    """

    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    cond: List[Dict[Any, ActionComponentSpec]] = element_field(
        signature=True,
        help=(
            "Contains a set of evaluation criteria that will be evaluated in "
            "order starting with the first evaluation criteria. The "
            "evaluation criteria is expressed using Meya's "
            "[template syntax](https://docs.meya.ai/docs/jinja2-syntax)."
        ),
    )
    default: ActionComponentSpec = element_field(
        help=(
            "This is the default action should none of the evaluation "
            "criteria evaluate to `True`."
        )
    )

    async def start(self) -> List[Entry]:
        for cond_branch in self.cond:
            cond_items = list(cond_branch.items())
            if len(cond_items) != 1:
                # TODO move this to validate()
                raise self.validation_error(
                    f"Cond expects one key and one value, not {cond_branch}"
                )
            [(cond_value, cond_action)] = cond_items
            if cond_value:
                return self.flow_control_action(cond_action)

        return self.flow_control_action(self.default)
