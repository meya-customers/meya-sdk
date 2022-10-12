from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.thread.entry import ThreadEntry
from typing import Any


@dataclass
class ThreadDataEntry(ThreadEntry):
    key: str = entry_field()
    value: Any = entry_field()
