from dataclasses import dataclass
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.entry.field import entry_field
from meya.log.scope import Scope


@dataclass
class LogEntry(Entry):
    scope: Scope = entry_field()
    timestamp: int = entry_field()

    @classmethod
    def get_entry_ledger(cls) -> str:
        return "log"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(trace_id=self.trace_id),
        )
