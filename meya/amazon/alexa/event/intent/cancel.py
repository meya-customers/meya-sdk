from dataclasses import dataclass
from meya.amazon.alexa.event.intent import AlexaIntentEvent


@dataclass
class AlexaCancelEvent(AlexaIntentEvent):
    pass
