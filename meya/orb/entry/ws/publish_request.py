from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.entry.ws.request import OrbWsRequestEntry
from meya.orb.entry.ws.user_data import OrbUserData
from typing import Any
from typing import Dict


@dataclass
class OrbWsPublishRequestEntry(OrbWsRequestEntry):
    event: Dict[str, Any] = entry_field(sensitive=True)
    user_data: Dict[str, OrbUserData] = entry_field(default_factory=dict)
    thread_id: str = entry_field()
