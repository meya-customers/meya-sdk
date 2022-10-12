from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.salesforce.live_agent.event import LiveAgentEvent
from typing import Optional


@dataclass
class LiveAgentSessionEstablishedEvent(LiveAgentEvent):
    agent_name: Optional[str] = entry_field()
    session_id: str = entry_field()
