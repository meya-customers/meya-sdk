from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.google.dialogflow.element.mixin import DialogflowMixin
from meya.text.trigger import TextTrigger
from meya.util.enum import SimpleEnum
from typing import Optional


@dataclass
class DialogflowTriggerResponse:
    result: str = response_field(sensitive=True)
    dialogflow_response: dict = response_field(sensitive=True)


class Expect(SimpleEnum):
    DIALOGFLOW = "dialogflow"


@dataclass
class DialogflowTrigger(TextTrigger, DialogflowMixin):
    expect: Optional[Expect] = element_field(
        signature=True, default=None, level=MetaLevel.ADVANCED
    )
