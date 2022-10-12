from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.salesforce.live_agent.event import LiveAgentEvent
from numbers import Real


@dataclass
class LiveAgentQueueUpdateEvent(LiveAgentEvent):
    position: Real = entry_field()
