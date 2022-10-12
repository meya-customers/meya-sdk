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
    Show buttons for the user to select.
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
        default=None, help="Question to send to the user"
    )
    buttons: List[ButtonElementSpecUnion] = element_field(
        signature=True, help="List of buttons that the user can select"
    )
    multi: bool = element_field(
        default=False, help="Whether multiple buttons can be selected"
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )
    label: Optional[str] = element_field(default=None)
    required: bool = element_field(default=False)
    error_message: str = element_field(
        default="Please select an option", level=MetaLevel.INTERMEDIATE
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
