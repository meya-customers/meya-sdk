from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.thread.entry import ThreadEntry


@dataclass
class ThreadUnlinkEntry(ThreadEntry):
    integration_id: str = entry_field()
    integration_thread_id: str = entry_field()
