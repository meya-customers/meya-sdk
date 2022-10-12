from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.form.event import FormEvent
from typing import Any
from typing import Dict


@dataclass
class FormSubmitEvent(FormEvent):
    fields: Dict[str, Any] = entry_field(sensitive=True)

    def to_transcript_text(self) -> str:
        parts = []
        for key, val in self.fields.items():
            parts.append(f"{key}: {val}")
        return "\n".join(parts)
