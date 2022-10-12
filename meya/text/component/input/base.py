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
    @dataclass
    class Response(FieldComponent.Response):
        result: str = response_field(sensitive=True)

    icon: Optional[IconElementSpecUnion] = element_field(default=None)
    placeholder: Optional[str] = element_field(default=None)
    default: Optional[str] = element_field(default=None)
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
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
