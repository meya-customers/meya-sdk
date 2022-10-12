from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.entry.ws import OrbWsEntry


@dataclass
class OrbWsResponseEntry(OrbWsEntry):
    status: int = entry_field()
