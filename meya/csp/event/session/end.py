from dataclasses import dataclass
from meya.csp.event import CspEvent
from meya.entry.field import entry_field


@dataclass
class SessionEndEvent(CspEvent):
    csp_integration_id: str = entry_field()
