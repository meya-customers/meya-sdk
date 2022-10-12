from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.widget.event.event import WidgetEvent
from typing import List
from typing import Optional


@dataclass
class ButtonAskEvent(WidgetEvent):
    buttons: List[ButtonEventSpec] = entry_field(sensitive_factory=list)
    multi: bool = entry_field(default=False)
    text: Optional[str] = entry_field(default=None, sensitive=True)
    label: Optional[str] = entry_field(default=None, sensitive=True)
    required: bool = entry_field(default=False)
    error: Optional[str] = entry_field(default=None, sensitive=True)

    def to_transcript_text(self) -> str:
        return "\n".join(
            [
                self.text or "...",
                *[
                    button.to_transcript_text()
                    for button in self.buttons + self.quick_replies
                ],
            ]
        )
