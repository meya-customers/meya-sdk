from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from typing import Optional


@dataclass
class ButtonClickEvent(Event):
    button_id: str = entry_field()
    text: Optional[str] = entry_field(default=None, sensitive=True)

    def to_transcript_text(self) -> str:
        return f"--> [{self.text or '...'}]"
