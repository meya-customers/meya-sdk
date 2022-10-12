from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.widget.event import WidgetEvent
from typing import Optional


@dataclass
class MediaEvent(WidgetEvent):
    url: str = entry_field(sensitive=True)
    text: Optional[str] = entry_field(default=None, sensitive=True)
    filename: Optional[str] = entry_field(default=None, sensitive=True)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(f"{self.url}")
