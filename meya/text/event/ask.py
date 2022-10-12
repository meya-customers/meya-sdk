from dataclasses import dataclass
from meya.text.event import TextEvent


@dataclass
class AskEvent(TextEvent):
    pass
