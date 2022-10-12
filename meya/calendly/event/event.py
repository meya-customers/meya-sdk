from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class CalendlyEvent(Event):
    booking_id: Optional[str] = entry_field()
    data: Dict[str, Any] = entry_field()  # TODO Use payload dataclasses
