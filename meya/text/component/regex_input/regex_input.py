from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.text.component.input.base import BaseTextInputComponent
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.widget.component.component import WidgetInputValidationError
from typing import Any
from typing import Optional
from typing import Union


@dataclass
class RegexInputComponent(BaseTextInputComponent, IgnorecaseMixin):
    """
    Get basic text input from the user using a form text input and validate
    the input using a specific regex pattern. This component can also be used
    as a text input widget in a page.

    ```yaml
    - regex_input: >
        ^
        ([A-Za-z]\d[A-Za-z])
        [ -]?
        (?P<second_part>\d[A-Za-z]\d)
        $
      label: Postal code
      required: true
      placeholder: Type your postal code here
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-regex_input.png" width="400"/>

    The regex input component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer)
    and set context data.

    Here is a more advanced example:

    ```yaml
    - regex_input: >
        ^
        ([A-Za-z]\d[A-Za-z])
        [ -]?
        (?P<second_part>\d[A-Za-z]\d)
        $
      label: Postal code
      required: true
      placeholder: Type your postal code here
      quick_replies:
        - text: Find my postal code
          action:
            flow: flow.find_postal_code
        - text: Talk to an agent
          action:
            flow: flow.agent
      context:
        foo: bar
      composer:
        focus: blur
        visibility: collapse
        collapse_placeholder: Ask a question
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-regex_input-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies** and **composer**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Input validation
    Once the user submits their input, it is evaluated against the specified
    regex pattern, and if the pattern matches then the component will store the
    value in `(@ flow.result )` in your app's [flow scope](https://docs.meya.ai/docs/scope#flow) data.
    If the pattern fails to match, then the regex component will display an
    error.

    Here is an example of the error:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-regex_input-2.png" width="400"/>

    ### Pages support
    This regex input component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the regex input component in a page:

    ```yaml
    - page:
      - regex_input: >
          ^
          ([A-Za-z]\d[A-Za-z])
          [ -]?
          (?P<second_part>\d[A-Za-z]\d)
          $
        label: Postal code
        required: true
        placeholder: Type your postal code here
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-regex_input-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    @dataclass
    class Response(BaseTextInputComponent.Response):
        result: Union[str, dict] = response_field(sensitive=True)

    regex_input: str = element_field(
        signature=True,
        help=(
            "The regex (regular expression) pattern to validate the user "
            "input against."
        ),
    )
    capture_groups: bool = element_field(
        default=False, help="Capture the regex groups."
    )
    ignorecase: Optional[bool] = element_field(
        default=None,
        help=(
            "Ignore the case of the user input when validating against the "
            "regex pattern."
        ),
    )
    error_message: str = element_field(
        default="Invalid input, please try again.",
        level=MetaLevel.INTERMEDIATE,
    )

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, str)
        match = RegexTrigger.search_regex(
            self.regex_input, self.input_data, self.ignorecase_default_true
        )
        if not match:
            raise WidgetInputValidationError(self.error_message)
        match_result, match_groups = match
        if not self.capture_groups:
            return match_result
        else:
            return match_groups
