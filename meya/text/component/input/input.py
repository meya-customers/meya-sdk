from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.text.component.input.base import BaseTextInputComponent
from meya.widget.component.component import WidgetInputValidationError
from typing import Any


@dataclass
class TextInputComponent(BaseTextInputComponent):
    """
    Get basic text input from the user using a form text input. This component
    is similar to the [text.ask.form](https://docs.meya.ai/reference/meya-text-component-ask-form) component
    but can also be used as a text input widget in a page.

    ```yaml
    - type: meya.text.component.input
      label: What is your name?
      required: true
      placeholder: Type your name here
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-input.png" width="400"/>

    The text input component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer)
    and set context data.

    Here is a more advanced example:

    ```yaml
    - type: meya.text.component.input
      label: Name
      required: true
      placeholder: Type your name here
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

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-input-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies** and **composer**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Input validation

    The text input component has no specific input validation and will capture any
    text input submitted by the user. However, if the `required` field is set
    to `true` then the input component will display an error if the user
    submits no value.

    Here is an example of the error:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-input-2.png" width="400"/>

    The user's input text is always stored in `(@ flow.result )` in your app's
    [flow scope](https://docs.meya.ai/docs/scope#flow) data.

    ### Pages support
    This text input component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the text input component in a page:

    ```yaml
    - page:
      - type: meya.text.component.input
        label: Name
        required: true
        placeholder: Type your name here
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-input-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    extra_alias: str = meta_field(value="text_input")
    error_message: str = element_field(
        default="Please enter a value.", level=MetaLevel.INTERMEDIATE
    )

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, str)
        if not self.input_data and self.required:
            raise WidgetInputValidationError(self.error_message)
        return self.input_data
