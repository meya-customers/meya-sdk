from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.facebook.wit.element.mixin import WitMixin
from meya.text.component.ask.catchall import AskCatchallComponent
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import Optional


@dataclass
class AskWitComposerComponentOkResponse:
    confidence: Real = response_field()
    result: str = response_field(sensitive=True)
    wit_response: dict = response_field(sensitive=True)
    ok: bool = response_field(default=True)


class Expect(SimpleEnum):
    WIT = "wit"


@dataclass
class WitAskComponent(AskCatchallComponent, WitMixin):
    expect: Optional[Expect] = element_field(signature=True, default=None)
