from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.widget.event.field import FieldEvent
from typing import List
from typing import Optional


@dataclass
class RatingGroupEventSpec:
    title: str
    fill: bool
    backfill: bool
    options: List[ButtonEventSpec]


@dataclass
class MultiRatingInputEvent(FieldEvent):
    groups: List[RatingGroupEventSpec] = entry_field(sensitive_factory=list)
    submit_button_text: Optional[str] = entry_field(default=None)
