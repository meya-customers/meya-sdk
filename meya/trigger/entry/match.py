from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.trigger.entry import TriggerEntry
from numbers import Real
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class TriggerMatchEntry(TriggerEntry):
    action_entry: Optional[Dict[str, Any]] = entry_field()
    confidence: Real = entry_field()
