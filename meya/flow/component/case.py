from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.text.ignorecase import IgnorecaseMixin
from meya.trigger.element import Trigger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class CaseComponent(Component, IgnorecaseMixin):
    """
    The case component is a more advanced branching component that allows you
    to match against multiple match values (this is similar to a switch
    statement in Javascript/Java/C/C++).

    ```yaml
    - value: (@ user.gender )
      case:
        male:
          jump: male
        female:
          jump: female
       default:
          jump: other
    ```

    **Note**, the values are matched literally, so in the case above the text
    stored in `(@ user.gender )` must exactly match either `male` or `female`
    to be a valid match.

    If you would like to match against multiple patterns, then check out the
    [`flow.match`](https://docs.meya.ai/reference/meya-flow-component-match)
    component.

    If you would like to match against multiple template evaluation criteria,
    then check out the [`flow.cond`](https://docs.meya.ai/reference/meya-flow-component-cond)
    component.
    """

    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    value: Any = element_field(
        default=None,
        help=(
            "Sets the value that needs to be matched against the multiple "
            "match values. If `value` is not defined, then the component will "
            "try use the value set in `(@ flow.result )`, if no value could "
            "be found then an error is raised."
        ),
    )
    ignorecase: Optional[bool] = element_field(
        default=None, help="Ignore the case of the value field."
    )
    case: Dict[Any, ActionComponentSpec] = element_field(
        signature=True,
        help=(
            "Contains a set of match values and actions that will be matched "
            "against the value defined in the `value` field. The action is a "
            "component reference that is called when `value` matches the "
            "match value."
        ),
    )
    default: ActionComponentSpec = element_field(
        help=(
            "This is the default action should `(@ flow.result )` not match "
            "any of the match values."
        )
    )

    async def start(self) -> List[Entry]:
        if self.value is None:
            # TODO use MISSING_FACTORY instead of None
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    "Case could not be evaluated because flow.result is "
                    "not set"
                )
            value = self.entry.data.get(Trigger.RESULT_KEY)
        else:
            value = self.value

        if self.ignorecase_default_true and isinstance(value, str):
            value = value.lower()

        for case_value, case_action in self.case.items():
            if self.ignorecase_default_true and isinstance(case_value, str):
                case_value = case_value.lower()

            if case_value == value:
                return self.flow_control_action(case_action)

        return self.flow_control_action(self.default)
