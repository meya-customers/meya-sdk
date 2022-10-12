from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.tile.event.choice import ChoiceInputEvent
from meya.tile.spec import ChoiceElementSpec
from meya.tile.spec import ChoiceElementSpecUnion
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
class ChoiceInputSubmitButtonElementSpec:
    text: str = "Submit"


@dataclass
class ChoiceInputComponent(FieldComponent):
    """
    Show choices for the user to select.
    """

    meta_level: float = meta_field(value=MetaLevel.BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])
    snippet_default: str = meta_field(
        value="""
            choices:
              - text: Yes
              - text: No
        """
    )

    choices: List[ChoiceElementSpecUnion] = element_field(
        signature=True, help="List of choices that the user can select"
    )
    multi: bool = element_field(
        default=False, help="Whether multiple choices are accepted"
    )
    submit: ChoiceInputSubmitButtonElementSpec = element_field(
        default_factory=ChoiceInputSubmitButtonElementSpec
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )
    error_message: str = element_field(
        default="Please select a choice", level=MetaLevel.INTERMEDIATE
    )

    async def build(self) -> List[Entry]:
        event = ChoiceInputEvent(
            choices=[
                ChoiceEventSpec(text=choice)
                if isinstance(choice, str)
                else ChoiceEventSpec(
                    text=choice.text,
                    default=choice.default,
                    disabled=choice.disabled,
                )
                for choice in self.choices
            ],
            multi=self.multi,
            submit_button_text=self.submit.text
            if self.mode == WidgetMode.STANDALONE
            else None,
        )
        return self.respond(event)

    async def validate_input_data(self) -> Any:
        if self.required and not self.input_data:
            raise WidgetInputValidationError(self.error_message)
        if self.multi:
            assert isinstance(self.input_data, list)
            return [
                self.validate_input_choice(input_choice)
                for input_choice in self.input_data
            ]
        else:
            return self.validate_input_choice(self.input_data)

    def validate_input_choice(self, input_choice: str) -> Any:
        assert isinstance(input_choice, str)
        if not input_choice:
            return input_choice
        choices = [
            ChoiceElementSpec(text=choice)
            if isinstance(choice, str)
            else choice
            for choice in self.choices
        ]
        valid_choices = {
            choice.text: choice for choice in choices if not choice.disabled
        }
        choice = valid_choices.get(input_choice)
        assert choice is not None
        if choice.value is not MISSING:
            input_choice = choice.value
        return input_choice
