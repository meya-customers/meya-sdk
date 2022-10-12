from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry.interactive import InteractiveEvent


@dataclass
class StatusEvent(InteractiveEvent):
    status: str = entry_field(sensitive=True)
    ephemeral: bool = entry_field(default=False)

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(
            f"[status: {self.status}]"
        )
