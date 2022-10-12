from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from meya.util.enum import SimpleEnum


class RejectReason(SimpleEnum):
    BUSY = "busy"
    REJECTED = "rejected"


@dataclass
class TwilioVoiceRejectEvent(Event):
    reason: RejectReason = entry_field()
