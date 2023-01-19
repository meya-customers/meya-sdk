from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.spec import ActionComponentSpec
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.trigger.element import Trigger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class MatchComponentResponse:
    result: Any = response_field()
    groups: dict = response_field()
    ok: bool = response_field()


@dataclass
class MatchComponent(Component, IgnorecaseMixin):
    """
    Match against multiple regex patterns.

    ```yaml
    # Match a/b/c/d
    - value: (@ flow.foo )
      match:
        (?P<a_group>a+):
          say: A (@ flow.groups.a_group )
        b.b:
          jump: b
        (cc)+:
          jump: c
      default:
        jump: d
    ```

    Each condition in the `match` field must contain a valid **action field**,
    meaning the field takes an action spec which maps to the [`ActionComponentSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/component/spec.py)
    Python class. This allows you to execute any component, but you will mostly
    use one of the flow control components.

    Also, Meya uses the [Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax) for all regex patterns.

    ### Match groups
    If your regex pattern defines any match groups, then these match groups
    will be available in flow scope under `(@ flow.groups )`.
    """

    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag])

    value: Any = element_field(
        default=None,
        help=(
            "Sets the value that needs to be matched against the multiple "
            "regex patterns. If `value` is not defined, then the component "
            "will try use the value set in `(@ flow.result )`, if no value "
            "could be found then an error is raised."
        ),
    )
    ignorecase: Optional[bool] = element_field(
        default=None, help="Ignore the case of the value field."
    )
    match: Dict[str, ActionComponentSpec] = element_field(
        signature=True,
        help=(
            "Contains a set of regex patterns and actions that will be "
            "evaluated against the value defined in the `value` field. The "
            "action is a component reference that is called when the `value` "
            "matches the regex pattern."
        ),
    )
    default: ActionComponentSpec = element_field(
        help=(
            "This the default action should the `value` not match any of the "
            "regex patterns."
        )
    )

    async def start(self) -> List[Entry]:
        if self.value is None:
            # TODO use MISSING_FACTORY instead of None
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    "Match could not be evaluated because flow.result is "
                    "not set"
                )
            value = self.entry.data.get(Trigger.RESULT_KEY)
        else:
            value = self.value
        best_length = -1
        best_action = self.default
        best_response = MatchComponentResponse(
            result=value, groups={}, ok=False
        )
        for match_regex, match_action in self.match.items():
            match = RegexTrigger.search_regex(
                match_regex, value, self.ignorecase_default_true
            )
            if match:
                match_result, match_groups = match
                length = len(match_result)
                if length > best_length:
                    best_length = length
                    best_action = match_action
                    best_response = MatchComponentResponse(
                        result=match_result, groups=match_groups, ok=True
                    )
        return self.flow_control_action(best_action, best_response)
