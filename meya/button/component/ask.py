from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from meya.button.event.ask import ButtonAskEvent
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.button.spec import ButtonType
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.icon.spec import IconElementSpecUnion
from meya.user.meta_tag import UserInputTag
from meya.widget.component import WidgetComponent
from meya.widget.component import WidgetInputValidationError
from typing import Any
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class ButtonAskComponent(WidgetComponent):
    """
    Show a set of buttons for the user to select.

    ```yaml
    - buttons:
      - text: Option 1
        result:
          key: 1
      - text: Option 2
        result:
          - two
          - two
      - text: Text 3
      - text: Link 4
        url: https://example.org/?n=5
      - text: Static 5
        button_id: _static_button
        context:
          product: marmalade
      - text: Menu 6
        menu:
          - text: Result 10
            result: 10
          - text: Result 11
            result: 11
          - text: Result 20
            result: 20
      - text: Disabled
        disabled: true
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-button-component-ask.png" width="400"/>

    The ask buttons components is also an interactive component which allows you to set [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the
    [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown), set context data and attach
    [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is another example including some interactive component features:

    ```yaml
    - ask: Choose **one** of the following options.
      buttons:
      - text: Option 1
        result:
          key: 1
      - text: Option 2
        result:
          - two
          - two
      - text: Text 3
      - text: Link 4
        url: https://example.org/?n=5
      - text: Static 5
        button_id: _static_button
        context:
          product: marmalade
      - text: Menu 6
        menu:
          - text: Result 10
            result: 10
          - text: Result 11
            result: 11
          - text: Result 20
            result: 20
      - text: Disabled
        disabled: true
      quick_replies:
        - Start over
        - text: Transfer to an agent
          action: next
      composer:
        visibility: collapse
        collapse_placeholder: Click to type
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-button-component-ask-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies**, **composer** and **markdown**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Button spec
    Each item in the `buttons` field must contain a valid **button spec** that
    specifies how the button should look and work. This **button spec** maps to
    the [`ButtonElementSpec`](https://github.com/meya-customers/meya-sdk/blob/main/meya/button/spec.py) Python class which is used by both buttons and
    quick replies.

    This makes quick replies very similar to buttons, but where they differ is
    that a quick reply can be configured to reply as a [text.say](https://docs.meya.ai/reference/meya-text-event-say) event instead of
    a [button.click](https://docs.meya.ai/reference/meya-button-event-click)
    event, whereas buttons can only create [button.click](https://docs.meya.ai/reference/meya-button-event-click)
    events.

    Check the [Buttons & Quick Replies guide](https://docs.meya.ai/docs/buttons-and-quick-replies) for more detail.

    ### Pages support
    The ask buttons component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the ask buttons component in a page:

    ```yaml
    - page:
      - buttons:
        - text: Option 1
          result:
            key: 1
        - text: Option 2
          result:
            - two
            - two
        - text: Text 3
        - text: Link 4
          url: https://example.org/?n=5
        - text: Static 5
          button_id: _static_button
          context:
            product: marmalade
        - text: Menu 6
          menu:
            - text: Result 10
              result: 10
            - text: Result 11
              result: 11
            - text: Result 20
              result: 20
        - text: Disabled
          disabled: true
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-button-component-ask-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.

    ### Input validation

    The buttons component can be marked as `required`, and when the `required`
    fields is set to `true` then the component will display an error if the
    user does not select a button. This is only applicable when using the
    buttons component in a page.

    Here is an example of the error:

    <img src="https://cdn.meya.ai/docs/images/meya-button-component-ask-page-1.png" width="400"/>

    """

    meta_name: str = meta_field(value="Buttons")
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/48-select/cursor.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])
    snippet_default: str = meta_field(
        value="""
            buttons:
              - text: Yes
                action: next
              - text: No
                action: next
        """
    )

    ask: Optional[str] = element_field(
        default=None, help="Question to send to the user."
    )
    buttons: List[ButtonElementSpecUnion] = element_field(
        signature=True,
        help=(
            "List of buttons that the user can select. Check the [button spec](https://docs.meya.ai/docs/buttons-and-quick-replies#button-spec) "
            "guide for more info on the different fields."
        ),
    )
    multi: bool = element_field(
        default=False,
        help=(
            "Whether multiple buttons can be selected at a time. This "
            "is similar to how a typical checkbox behaves."
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
    label: Optional[str] = element_field(
        default=None,
        help="The label displayed above the set of buttons.",
    )
    required: bool = element_field(
        default=False,
        help="Specifies whether one of the buttons must be selected or not.",
    )
    error_message: str = element_field(
        default="Please select an option",
        level=MetaLevel.INTERMEDIATE,
        help=(
            "The error message that is displayed when the a selection is "
            "required."
        ),
    )

    @property
    def skip_triggers(self) -> bool:
        return self.input_validation.ok

    async def build(self) -> List[Entry]:
        buttons, triggers = ButtonEventSpec.from_element_spec_union_list(
            self.buttons, skip_triggers=self.skip_triggers
        )
        event = ButtonAskEvent(
            buttons=buttons,
            multi=self.multi,
            text=self.ask,
            label=self.label,
            required=self.required,
            error=self.input_validation.error,
        )
        return self.respond(event, *triggers)

    async def validate_input_data(self) -> Any:
        if self.required and not self.input_data:
            raise WidgetInputValidationError(self.error_message)
        if self.multi:
            assert isinstance(self.input_data, list)
            return [
                self.validate_input_button(input_button)
                for input_button in self.input_data
            ]
        else:
            return self.validate_input_button(self.input_data)

    def validate_input_button(self, input_button: Any) -> Any:
        assert isinstance(input_button, str)
        if not input_button:
            return input_button
        buttons = [
            ButtonElementSpec(text=button)
            if isinstance(button, str)
            else button
            for button in self.buttons
        ]
        valid_buttons = {
            button.text: button
            for button in buttons
            if button.computed_type == ButtonType.TEXT
        }
        button = valid_buttons.get(input_button)
        assert button is not None
        if button.value is not MISSING:
            input_button = button.value
        return input_button
