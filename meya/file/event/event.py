from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.icon.spec import IconEventSpec
from meya.media.event import MediaEvent
from typing import Optional


@dataclass
class FileEvent(MediaEvent):
    filename: str = entry_field(sensitive=True)
    icon: Optional[IconEventSpec] = entry_field(default=None)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(
            f"[{self.filename}] {self.url}"
        )
