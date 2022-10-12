from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.lifecycle.event.event import LifecycleEvent
from typing import Optional


@dataclass
class ChatOpenEvent(LifecycleEvent):
    lifecycle_id: str = entry_field(default="chat_open")
    text: Optional[str] = entry_field(default=None)
