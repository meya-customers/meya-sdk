from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.salesforce.live_agent.event import LiveAgentEvent


@dataclass
class LiveAgentAgentConferenceLeaveEvent(LiveAgentEvent):
    agent_name: str = entry_field()
    session_id: str = entry_field()
