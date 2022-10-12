from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event


@dataclass
class FormEvent(Event):
    form_id: str = entry_field()
