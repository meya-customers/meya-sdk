from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.text.component.ask import AskValidationError
from meya.text.component.ask.catchall import AskCatchallComponent
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.text.trigger.regex import RegexTriggerResponse
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from typing import Any
from typing import Optional


@dataclass
class AskRegexComposerComponentOkResponse:
    result: str = response_field(sensitive=True)
    groups: dict = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class AskRegexComponent(AskCatchallComponent, IgnorecaseMixin):
    """
    Get basic text input from the user and validate the input against the
    specified regex pattern.

    ```yaml
    - ask: What's your postal code?
      regex: >
        ^
        ([A-Za-z]\d[A-Za-z])
        [ -]?
        (?P<second_part>\d[A-Za-z]\d)
        $
      error_message: Invalid postal code, please try again.
      retries: .inf
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-ask_regex.png" width="400"/>

    ### Input validation
    Once the user submits their input, it is evaluated against the specified
    regex pattern, and if the pattern matches then the component will store the
    value in `(@ flow.result )` in your app's [flow scope](https://docs.meya.ai/docs/scope#flow) data. If
    you use regex groups the group results will also be stored in the flow scope
    in `(@ flow.groups )`.

    Note, Meya uses the [Python regular expression syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax) for all regex patterns.

    ### Retries
    By default the component will retry until the user's input matches the input.
    However, you can override this by setting an explicit `retries` value.

    The component will continue to the next flow step once the retry value has
    been reached. In this case `(@ flow.result )` will be `None`.
    """

    regex: str = element_field(
        signature=True,
        help=(
            "The regex (regular expression) pattern to validate the user "
            "input against."
        ),
    )
    ignorecase: Optional[bool] = element_field(
        default=None,
        help=(
            "Ignore the case of the user input when validating against the "
            "regex pattern."
        ),
    )

    def trigger(self, data: Any = None) -> TriggerActivateEntry:
        return RegexTrigger(
            regex=self.regex,
            ignorecase=self.ignorecase,
            confidence=self.confidence,
            action=self.get_next_action(data=data),
        ).activate()

    async def next_response(self) -> Any:
        encrypted_trigger_response = from_dict(
            RegexTriggerResponse, self.entry.data
        )
        match_result = encrypted_trigger_response.result
        match_groups = encrypted_trigger_response.groups

        if self.catchall and not match_result:
            raise AskValidationError()

        return AskRegexComposerComponentOkResponse(
            result=match_result, groups=match_groups
        )
