from dataclasses import dataclass
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.entry.field import entry_field


@dataclass
class UserEntry(Entry):
    user_id: str = entry_field()

    @classmethod
    def get_entry_ledger(cls) -> str:
        return "user"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(user_id=self.user_id),
        )
