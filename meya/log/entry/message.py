from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.log.entry import LogEntry
from meya.log.level import Level
from typing import Any
from typing import Dict
from typing import List


@dataclass
class LogMessageEntry(LogEntry):
    args: List[Any] = entry_field(default_factory=list)
    context: Dict[str, Any] = entry_field(default_factory=dict)
    level: Level = entry_field()
    message: str = entry_field()
