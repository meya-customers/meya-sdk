from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.tile.spec import ChoiceEventSpec
from meya.widget.event.field import FieldEvent
from typing import List
from typing import Optional


@dataclass
class ChoiceInputEvent(FieldEvent):
    choices: List[ChoiceEventSpec] = entry_field(sensitive_factory=list)
    multi: bool = entry_field(default=False)
    submit_button_text: Optional[str] = entry_field(default=None)
