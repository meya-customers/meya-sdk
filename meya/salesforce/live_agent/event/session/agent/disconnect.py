from dataclasses import dataclass
from meya.salesforce.live_agent.event import LiveAgentEvent


@dataclass
class LiveAgentAgentDisconnectEvent(LiveAgentEvent):
    pass
