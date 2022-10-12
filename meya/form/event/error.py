from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent
from meya.form.event import FormEvent
from typing import Dict


@dataclass
class FormErrorEvent(FormEvent, InteractiveEvent):
    fields: Dict[str, str] = entry_field(sensitive=True)
