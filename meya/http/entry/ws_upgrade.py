from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.entry import HttpEntry
from typing import Any
from typing import Dict


@dataclass
class HttpWsUpgradeEntry(HttpEntry):
    context: Dict[str, Any] = entry_field(default_factory=dict)
