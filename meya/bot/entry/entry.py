from dataclasses import dataclass
from meya.entry import Entry
from meya.entry.entry import EntryRef
from meya.entry.field import entry_field


@dataclass
class BotEntry(Entry):
    bot_id: str = entry_field(default_missing=True)
    thread_id: str = entry_field(default_missing=True)

    @classmethod
    def get_entry_ledger(cls) -> str:
        return "bot"

    def to_ref(self) -> EntryRef:
        return EntryRef(
            ledger=self.entry_ledger,
            id=self.entry_id,
            data=dict(bot_id=self.bot_id, thread_id=self.thread_id),
        )
