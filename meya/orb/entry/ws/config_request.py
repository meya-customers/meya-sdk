from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.entry.ws.request import OrbWsRequestEntry
from typing import Any
from typing import Dict


@dataclass
class OrbWsConfigRequestEntry(OrbWsRequestEntry):
    key: str = entry_field()
    value: Dict[str, Any] = entry_field(sensitive=True)
    thread_id: str = entry_field()
