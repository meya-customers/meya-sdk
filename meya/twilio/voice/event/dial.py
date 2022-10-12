from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event


@dataclass
class TwilioVoiceDialEvent(Event):
    number: str = entry_field()
