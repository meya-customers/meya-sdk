from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from typing import Optional


@dataclass
class HeroEvent(InteractiveEvent):
    description: Optional[str] = entry_field(default=None, sensitive=True)
    title: Optional[str] = entry_field(default=None, sensitive=True)
