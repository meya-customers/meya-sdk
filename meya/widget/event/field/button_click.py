from dataclasses import dataclass
from meya.button.event.click import ButtonClickEvent
from meya.entry.field import entry_field
from typing import Any


@dataclass
class FieldButtonClickEvent(ButtonClickEvent):
    field_id: str = entry_field()
    input_data: Any = entry_field(sensitive=True)
