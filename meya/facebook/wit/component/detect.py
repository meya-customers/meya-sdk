from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.facebook.wit.element.mixin import WitMixin
from numbers import Real
from typing import Optional


@dataclass
class WitDetectComponentOkResponse:
    confidence: Optional[Real] = response_field(default=None)
    result: Optional[str] = response_field(sensitive=True, default=None)
    wit_response: Optional[dict] = response_field(sensitive=True, default=None)
    ok: bool = response_field(default=True)


@dataclass
class WitDetectComponent(BaseApiComponent, WitMixin):
    detect_wit: str = element_field(
        signature=True,
        help="The phrase to be sent to Wit for intent detection.",
    )
