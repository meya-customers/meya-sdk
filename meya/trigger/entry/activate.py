from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.trigger.entry import TriggerEntry
from typing import Any
from typing import Dict


@dataclass
class TriggerActivateEntry(TriggerEntry):
    spec: Dict[str, Any] = entry_field()
