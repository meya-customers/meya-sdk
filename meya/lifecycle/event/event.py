from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from typing import Optional


@dataclass
class LifecycleEvent(Event):
    lifecycle_id: str = entry_field()
    text: Optional[str] = entry_field()
