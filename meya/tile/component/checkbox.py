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

    checkbox: str = element_field(signature=True, help="Text for the checkbox")
    default: Optional[bool] = element_field(default=None)
    submit: CheckboxInputSubmitButtonElementSpec = element_field(
        default_factory=CheckboxInputSubmitButtonElementSpec
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
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
