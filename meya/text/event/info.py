from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.widget.event import WidgetEvent


@dataclass
class InfoEvent(WidgetEvent):
    info: str = entry_field(sensitive=True)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(f"[info: {self.info}]")
