from dataclasses import dataclass
from meya.button.event.click import ButtonClickEvent
from meya.entry.field import entry_field
from typing import Any
from typing import List


@dataclass
class PageButtonClickEvent(ButtonClickEvent):
    page_id: str = entry_field()
    input_data: List[Any] = entry_field(sensitive=True)
