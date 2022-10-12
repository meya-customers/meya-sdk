from dataclasses import dataclass
from meya.presence.event import PresenceEvent


@dataclass
class TypingEvent(PresenceEvent):
    pass
