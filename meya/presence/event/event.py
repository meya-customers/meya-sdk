from dataclasses import dataclass
from meya.entry.entry import EntryRef
from meya.event.entry import Event


@dataclass
class PresenceEvent(Event):
    @classmethod
    def get_entry_ledger(cls) -> str:
        return "presence"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(thread_id=self.thread_id),
        )
