from dataclasses import dataclass
from meya.csp.event import CspEvent


@dataclass
class AgentRequestErrorEvent(CspEvent):
    pass
