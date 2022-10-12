from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class PageEvent(InteractiveEvent):
    page_id: str = entry_field()
    widgets: List[Dict[str, Any]] = entry_field(sensitive_factory=list)
    input_data: Optional[List[Any]] = entry_field(default=None, sensitive=True)
    submit_button_id: Optional[str] = entry_field(default=None)
    submit_button_text: Optional[str] = entry_field(default=None)
    extra_buttons: List[ButtonEventSpec] = entry_field(
        default_factory=list, sensitive_factory=list
    )
    ok: bool = entry_field()
