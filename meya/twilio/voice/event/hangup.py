from dataclasses import dataclass
from meya.event.entry import Event


@dataclass
class TwilioVoiceHangupEvent(Event):
    pass
