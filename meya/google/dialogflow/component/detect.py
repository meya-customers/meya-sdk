from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.google.dialogflow.element.mixin import DialogflowMixin
from numbers import Real


@dataclass
class DialogflowDetectComponentOkResponse:
    confidence: Real = response_field()
    result: str = response_field()
    dialogflow_response: dict = response_field()
    ok: bool = response_field(default=True)


@dataclass
class DialogflowDetectComponentErrorResponse:
    ok: bool = response_field(default=False)


@dataclass
class DialogflowDetectComponent(BaseApiComponent, DialogflowMixin):
    detect_dialogflow: str = element_field(signature=True)
