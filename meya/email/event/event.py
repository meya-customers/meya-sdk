from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.text.event import TextEvent
from typing import Optional


@dataclass
class EmailEvent(TextEvent):
    message_id: Optional[str] = entry_field(default=None, sensitive=True)
    subject: Optional[str] = entry_field(default=None, sensitive=True)
    html: Optional[str] = entry_field(default=None, sensitive=True)
