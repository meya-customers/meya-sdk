from dataclasses import dataclass
from meya.amazon.alexa.event import AlexaEvent
from meya.entry.field import entry_field


@dataclass
class AlexaIntentEvent(AlexaEvent):
    name: str = entry_field()
