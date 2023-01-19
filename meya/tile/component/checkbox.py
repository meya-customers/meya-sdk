from dataclasses import dataclass
from dataclasses import field
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.tile.event.choice import ChoiceInputEvent
from meya.tile.spec import ChoiceEventSpec
from meya.user.meta_tag import UserInputTag
from meya.widget.component import WidgetInputValidationError
from meya.widget.component.component import WidgetMode
from meya.widget.component.field import FieldComponent
from typing import Any
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class CheckboxInputSubmitButtonElementSpec:
    text: str = "Submit"


@dataclass
class CheckboxInputComponent(FieldComponent):
    """
    Show a checkbox for the user to check.

    Here is a basic example:

    ```yaml
    - checkbox: Accept terms & conditions
      required: true
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-checkbox.png" width="400"/>

    The ask tiles component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer)
    and set context data.

    Here is a more advanced example:

    ```yaml
    - checkbox: Accept terms & conditions
      required: true
      quick_replies:
        - text: Discover earth
          action:
            flow: flow.earth
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

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-checkbox-1.png" width="400"/>

    **Note**, this component is only compatible with the Meya Orb Web/Mobile SDK.
    Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Input validation

    If the `required` field is set to `true` then the input component will
    display an error if the user submits no value.

    Here is an example of the error:

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-checkbox-2.png" width="400"/>

    The user's input text is always stored in `(@ flow.result )` in your app's
    [flow scope](https://docs.meya.ai/docs/scope#flow) data.

    ### Pages support
    This checkbox component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the text input component in a page:

    ```yaml
    - page:
      - checkbox: Accept terms & conditions
        required: true
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-tile-component-checkbox-3.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    @dataclass
    class Response:
        result: bool = response_field(sensitive=True)

    meta_level: float = meta_field(value=MetaLevel.BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])
    snippet_default: str = meta_field(
        value="""
            checkbox: Accept
        """
    )

    checkbox: str = element_field(
        signature=True, help="Text for the checkbox field."
    )
    default: Optional[bool] = element_field(
        default=None,
        help=(
            "Specify a default value if this field is not required, and the "
            "user does not submit a value."
        ),
    )
    submit: CheckboxInputSubmitButtonElementSpec = element_field(
        default_factory=CheckboxInputSubmitButtonElementSpec,
        help=(
            "The text of the submit button which defaults to `Submit` if not "
            "specified. Check the [`CheckboxInputSubmitButtonElementSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/tile/component/checkbox.py) "
            "Python class to see what each field does."
        ),
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help=(
            "The composer spec that allows you to control the Orb's input "
            "composer. Check the "
            "[Composer](https://docs.meya.ai/docs/composer) guide for more "
            "info."
        ),
    )
    error_message: str = element_field(
        default="Please check this box", level=MetaLevel.INTERMEDIATE
    )

    async def build(self) -> List[Entry]:
        event = ChoiceInputEvent(
            choices=[
                ChoiceEventSpec(text=self.checkbox, default=self.default)
            ],
            multi=True,
            submit_button_text=self.submit.text
            if self.mode == WidgetMode.STANDALONE
            else None,
        )
        return self.respond(event)

    async def validate_input_data(self) -> Any:
        if self.required and not self.input_data:
            raise WidgetInputValidationError(self.error_message)
        return bool(self.input_data)
