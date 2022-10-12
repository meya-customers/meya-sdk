from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from meya.form.event import FormEvent
from meya.form.spec import SelectOptionEventSpec
from meya.icon.spec import IconEventSpec
from meya.util.enum import SimpleEnum
from typing import Any
from typing import List
from typing import Optional


class FieldType(SimpleEnum):
    EMAIL = "email"
    TEXT = "text"
    SELECT = "select"


@dataclass
class Field:
    name: str = entry_field()
    autocomplete: Optional[str] = entry_field(default=None)
    icon: Optional[IconEventSpec] = entry_field(default=None)
    label: str = entry_field()
    no_results_text: Optional[str] = entry_field(default=None)
    placeholder: Optional[str] = entry_field(default=None)
    required: Optional[bool] = entry_field(default=None)
    type: FieldType = entry_field()
    custom: Optional[bool] = entry_field(default=None)
    search: Optional[bool] = entry_field(default=None)
    multi: Optional[bool] = entry_field(default=None)
    options: Optional[List[SelectOptionEventSpec]] = entry_field(default=None)
    default: Any = entry_field(default=None)


@dataclass
class FormAskEvent(FormEvent, InteractiveEvent):
    fields: List[Field] = entry_field(sensitive_factory=list)
    form_id: str = entry_field()
    text: Optional[str] = entry_field(default=None, sensitive=True)

    def to_transcript_text(self) -> str:
        parts = []
        if self.text:
            parts.append(self.text)
        for field in self.fields:
            if field.label:
                parts.append(f"{field.label}: ______")
        return self._add_quick_reply_transcript_text("\n".join(parts))
