from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from typing import Optional


@dataclass
class TextEvent(InteractiveEvent):
    text: Optional[str] = entry_field(sensitive=True)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(self.text or "...")
