from dataclasses import dataclass
from meya.presence.event.typing import TypingEvent


@dataclass
class TypingOffEvent(TypingEvent):
    pass
