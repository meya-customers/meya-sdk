from dataclasses import dataclass
from dataclasses import field
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.text.event.input import TextInputEvent
from meya.text.event.input import TextInputType
from meya.widget.component.field import FieldComponent
from typing import ClassVar
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class BaseTextInputComponent(FieldComponent):
    """
    This is the base text input component that is used by **all** other text
    input field components, and defines some common fields that are used by
    all text input components.

    This is base component and should **not** be used directly in your BFML.

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input using field components.
    """

    @dataclass
    class Response(FieldComponent.Response):
        result: str = response_field(sensitive=True)

    icon: Optional[IconElementSpecUnion] = element_field(
        default=None,
        help=(
            "The icon spec or URL to use for the input field. See the "
            "[Icons](https://docs.meya.ai/docs/icons) guide for more info."
        ),
    )
    placeholder: Optional[str] = element_field(
        default=None,
        help=(
            "The input field's placeholder text. This is displayed when the"
            "field has not user specified text."
        ),
    )
    default: Optional[str] = element_field(
        default=None, help="The input's default value."
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

    input_type: ClassVar[TextInputType] = TextInputType.TEXT

    async def build(self) -> List[Entry]:
        event = TextInputEvent(
            default=self.default,
            icon=IconEventSpec.from_element_spec(self.icon),
            placeholder=self.placeholder,
            type=self.input_type,
        )
        return self.respond(event)
