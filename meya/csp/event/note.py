from dataclasses import dataclass
from meya.csp.event.event import CspEvent
from meya.entry.field import entry_field


@dataclass
class NoteEvent(CspEvent):
    text: str = entry_field(sensitive=True)

    def to_transcript_text(self) -> str:
        return self.text
