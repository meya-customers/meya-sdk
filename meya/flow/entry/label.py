from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.flow.entry import FlowEntry


@dataclass
class FlowLabelEntry(FlowEntry):
    index: int = entry_field()
    label: str = entry_field()
