from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.salesforce.live_agent.event import LiveAgentEvent


@dataclass
class LiveAgentChatRequestEvent(LiveAgentEvent):
    session_id: str = entry_field()
