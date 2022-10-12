from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry import Event
from meya.event.header_spec import HeaderEventSpec
from meya.text.markdown import MarkdownEventSpec
from typing import List


@dataclass
class InteractiveEvent(Event):
    composer: ComposerEventSpec = entry_field(
        default_missing=True,
        default_factory=ComposerEventSpec,
        sensitive_factory=ComposerEventSpec,
    )
    quick_replies: List[ButtonEventSpec] = entry_field(
        default_missing=True, default_factory=list, sensitive_factory=list
    )
    header: HeaderEventSpec = entry_field(
        default_missing=True,
        default_factory=HeaderEventSpec,
        sensitive_factory=HeaderEventSpec,
    )
    markdown: MarkdownEventSpec = entry_field(
        default_missing=True, default_factory=list
    )

    def to_transcript_text(self) -> str:
        return self._add_quick_reply_transcript_text(
            super().to_transcript_text()
        )

    def _add_quick_reply_transcript_text(self, text: str) -> str:
        return "\n".join(
            [
                text,
                *[
                    button.to_transcript_text()
                    for button in self.quick_replies
                ],
            ]
        )
