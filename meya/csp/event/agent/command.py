from dataclasses import dataclass
from meya.csp.event import CspEvent
from meya.entry.field import entry_field


@dataclass
class AgentCommandEvent(CspEvent):
    text: str = entry_field(sensitive=True)
