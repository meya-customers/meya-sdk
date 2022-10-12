from dataclasses import dataclass
from dataclasses import field
from meya.db.view.db import DbView
from meya.event.entry import Event
from typing import List


@dataclass
class HistoryView:
    db: DbView = field(init=False)

    def __post_init__(self):
        self.db = DbView.current.try_get()

    async def get_thread_events(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
    ) -> List[Event]:
        encrypted_events = await self.get_encrypted_thread_events(
            thread_id, end, start, count
        )
        return [
            await self.db.try_decrypt_sensitive_entry(encrypted_event)
            for encrypted_event in encrypted_events
        ]

    async def get_encrypted_thread_events(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
    ) -> List[Event]:
        return await self.db.query_event_ledger(thread_id, end, start, count)

    async def get_redacted_thread_events(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
    ) -> List[Event]:
        encrypted_events = await self.get_encrypted_thread_events(
            thread_id, end, start, count
        )
        return [
            self.db.redact_sensitive_entry(encrypted_event)
            for encrypted_event in encrypted_events
        ]
