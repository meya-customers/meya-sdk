from dataclasses import dataclass
from dataclasses import field
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.facebook.wit.element.mixin import WitMixin
from meya.icon.spec import IconElementSpecUnion
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import Optional


@dataclass
class AskWitFormComponentOkResponse:
    confidence: Real = response_field()
    result: str = response_field(sensitive=True)
    wit_response: dict = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


class Expect(SimpleEnum):
    WIT = "wit"


@dataclass
class WitAskFormComponent(InteractiveComponent, WitMixin):
    expect: Optional[Expect] = element_field(signature=True, default=None)
    ask_form: Optional[str] = element_field(
        signature=True,
        default=None,
        help="Phrase to be sent to Wit AI for intent detection",
    )
    icon: Optional[IconElementSpecUnion] = element_field(
        default=None, help="Icon will be shown on field left side"
    )
    label: str = element_field(
        default="Text",
        help="This text will be shown on top left of the form field",
    )
    field_name: Optional[str] = element_field(default="text")
    autocomplete: Optional[str] = element_field(default="off")
    placeholder: Optional[str] = element_field(default=None)
    retries: Real = element_field(default=float("inf"))
    error_message: str = element_field(default="Invalid")
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )
