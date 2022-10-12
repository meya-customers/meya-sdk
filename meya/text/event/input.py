from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.icon.spec import IconEventSpec
from meya.util.enum import SimpleEnum
from meya.widget.event.field import FieldEvent
from typing import Optional


class TextInputType(SimpleEnum):
    TEXT = "text"
    EMAIL = "email"


@dataclass
class TextInputEvent(FieldEvent):
    icon: Optional[IconEventSpec] = entry_field(default=None)
    placeholder: Optional[str] = entry_field(default=None, sensitive=True)
    default: Optional[str] = entry_field(default=None, sensitive=True)
    type: TextInputType = entry_field()
