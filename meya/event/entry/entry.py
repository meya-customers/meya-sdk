from dataclasses import dataclass
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.entry.field import entry_field
from typing import Any
from typing import Dict


@dataclass
class Event(Entry):
    user_id: str = entry_field(default_missing=True)
    thread_id: str = entry_field(default_missing=True)
    integration_id: str = entry_field(default_missing=True)
    context: Dict[str, Any] = entry_field(
        default_factory=dict, default_missing=True, sensitive_factory=dict
    )

    def to_transcript_text(self) -> str:
        return f"<{self.get_entry_type()}>"

    @classmethod
    def get_entry_ledger(cls) -> str:
        return "event"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(thread_id=self.thread_id),
        )
