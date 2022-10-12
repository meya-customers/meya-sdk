from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.google.dialogflow.element.mixin import DialogflowMixin
from meya.text.component.input.base import BaseTextInputComponent
from numbers import Real
from typing import Optional


@dataclass
class DialogflowInputComponentResult:
    confidence: Real
    intent: str
    dialogflow_response: dict


@dataclass
class DialogflowInputComponent(BaseTextInputComponent, DialogflowMixin):
    @dataclass
    class Response(BaseTextInputComponent.Response):
        result: Optional[DialogflowInputComponentResult] = response_field(
            sensitive=True
        )

    extra_alias: str = meta_field(value="dialogflow_input")
    error_message: str = element_field(
        default="Invalid input, please try again.",
        level=MetaLevel.INTERMEDIATE,
    )
