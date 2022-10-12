from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.google.dialogflow.element.mixin import DialogflowMixin
from meya.text.component.ask.catchall import AskCatchallComponent
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import Optional


@dataclass
class AskDialogflowComposerComponentOkResponse:
    confidence: Real = response_field()
    result: str = response_field(sensitive=True)
    dialogflow_response: dict = response_field(sensitive=True)
    ok: bool = response_field(default=True)


class Expect(SimpleEnum):
    DIALOGFLOW = "dialogflow"


@dataclass
class DialogflowAskComponent(AskCatchallComponent, DialogflowMixin):
    expect: Optional[Expect] = element_field(
        signature=True, default=None, level=MetaLevel.ADVANCED
    )
