from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.flow.entry import FlowEntry
from typing import Optional


@dataclass
class FlowStartEntry(FlowEntry):
    label: Optional[str] = entry_field()
