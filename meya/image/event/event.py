from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.media.event import MediaEvent
from typing import Optional


@dataclass
class ImageEvent(MediaEvent):
    alt: Optional[str] = entry_field(default=None, sensitive=True)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(f"[image] {self.url}")
