from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.flow.entry import FlowEntry


@dataclass
class FlowNextEntry(FlowEntry):
    index: int = entry_field()
