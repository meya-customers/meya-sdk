from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from typing import List


@dataclass
class RatingEvent(InteractiveEvent):
    title: str = entry_field(sensitive=True)
    fill: bool = entry_field()
    backfill: bool = entry_field()
    options: List[ButtonEventSpec] = entry_field(sensitive_factory=list)
