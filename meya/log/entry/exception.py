from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.log.entry import LogEntry
from typing import Any
from typing import Dict
from typing import List


@dataclass
class LogExceptionEntry(LogEntry):
    context: Dict[str, Any] = entry_field(default_factory=dict)
    exception: str = entry_field()
    exception_type: str = entry_field()
    stack_trace: List[List[str]] = entry_field()
