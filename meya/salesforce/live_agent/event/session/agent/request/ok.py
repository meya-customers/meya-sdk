from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.salesforce.live_agent.event import LiveAgentEvent
from numbers import Real
from typing import Optional


@dataclass
class LiveAgentAgentRequestOkEvent(LiveAgentEvent):
    queue_position: Optional[Real] = entry_field()
    session_id: str = entry_field()
    visitor_id: str = entry_field()
