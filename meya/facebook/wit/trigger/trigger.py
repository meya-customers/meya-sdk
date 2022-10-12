from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.facebook.wit.element.mixin import WitMixin
from meya.text.trigger import TextTrigger
from meya.util.enum import SimpleEnum
from typing import Optional


@dataclass
class WitTriggerResponse:
    result: str = response_field(sensitive=True)
    wit_response: dict = response_field(sensitive=True)


class Expect(SimpleEnum):
    WIT = "wit"


@dataclass
class WitTrigger(TextTrigger, WitMixin):
    expect: Optional[Expect] = element_field(signature=True, default=None)
