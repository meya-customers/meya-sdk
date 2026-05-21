from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.icon.spec import IconEventSpec
from meya.widget.event.field import FieldEvent
from typing import Optional


@dataclass
class DateInputEvent(FieldEvent):
    icon: Optional[IconEventSpec] = entry_field(default=None)
    default: Optional[str] = entry_field(default=None, sensitive=True)
    min: Optional[str] = entry_field(default=None)
    max: Optional[str] = entry_field(default=None)
