from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.flow.entry import FlowEntry


@dataclass
class FlowEndEntry(FlowEntry):
    index: int = entry_field()
