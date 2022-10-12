from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.facebook.wit.element.mixin import WitMixin
from meya.text.component.input.base import BaseTextInputComponent
from numbers import Real
from typing import Optional


@dataclass
class WitInputComponentResult:
    confidence: Real
    intent: str
    wit_response: dict


@dataclass
class WitInputComponent(BaseTextInputComponent, WitMixin):
    @dataclass
    class Response(BaseTextInputComponent.Response):
        result: Optional[WitInputComponentResult] = response_field(
            sensitive=True
        )

    extra_alias: str = meta_field(value="wit_input")
    error_message: str = element_field(
        default="Invalid input, please try again.",
        level=MetaLevel.INTERMEDIATE,
    )
