from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.direction import Direction
from meya.orb.entry.ws import OrbWsEntry
from typing import Any
from typing import Dict


@dataclass
class OrbWsRequestEntry(OrbWsEntry):
    direction: Direction = entry_field(default_missing=True)
    context: Dict[str, Any] = entry_field(default_factory=dict)
