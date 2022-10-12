from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event
from numbers import Real
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class IdentifyEvent(Event):
    data: Dict[str, Any] = entry_field()
    timestamp: Optional[Real] = entry_field()
