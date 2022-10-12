from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.flow.entry import FlowEntry


@dataclass
class FlowJumpEntry(FlowEntry):
    label: str = entry_field()
