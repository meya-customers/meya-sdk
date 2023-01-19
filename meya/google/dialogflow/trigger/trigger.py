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
    """
    This trigger will call your Dialogflow agent's "detect intent" API with
    the user's input text and will match if the intent confidence threshold
    is reached.

    https://docs.meya.ai/docs/triggers-1#dialogflow-trigger
    """

    expect: Optional[Expect] = element_field(
        signature=True,
        default=None,
        level=MetaLevel.ADVANCED,
        help="Set to `dialogflow` to match Dialogflow intents.",
    )
