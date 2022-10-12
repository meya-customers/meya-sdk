from dataclasses import dataclass
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.entry.field import entry_field


@dataclass
class WsEntry(Entry):
    sensitive: bool = entry_field(default=True)
    request_id: str = entry_field()

    @classmethod
    def get_entry_ledger(cls) -> str:
        return "ws"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(request_id=self.request_id),
        )
