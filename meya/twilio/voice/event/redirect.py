from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event


@dataclass
class TwilioVoiceRedirectEvent(Event):
    url: str = entry_field()
    method: str = entry_field()
