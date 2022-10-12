from dataclasses import MISSING
from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.db.view.user import UserType
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry import Event
from meya.event.entry.interactive import InteractiveEvent
from meya.event.header_spec import HeaderEventSpec
from meya.integration.element import Integration
from meya.presence.event.typing.typing import TypingEvent
from meya.text.markdown import MarkdownElementSpecUnion
from meya.text.markdown import MarkdownEventSpecHelper
from typing import List


@dataclass
class InteractiveIntegration(Integration):
    is_abstract: bool = meta_field(value=True)

    markdown: MarkdownElementSpecUnion = element_field(default=False)
    typing: bool = element_field(
        default=True,
        help=(
            "When set to 'False', all typing indicators received by the "
            "integration will be ignored."
        ),
    )

    async def accept_sensitive(self) -> bool:
        return await self.accept()

    def post_process_all(self, entries: List[Entry]) -> List[Entry]:
        entries = super().post_process_all(entries)
        if not self.typing:
            return [
                entry
                for entry in entries
                if not isinstance(entry, TypingEvent)
            ]
        else:
            return entries

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        super().post_process(entry, extra_entries)

        if isinstance(entry, InteractiveEvent):
            if entry.quick_replies is MISSING:
                entry.quick_replies = []

            if entry.composer is MISSING:
                entry.composer = ComposerEventSpec()

            if entry.markdown is MISSING:
                entry.markdown = MarkdownEventSpecHelper.from_element_spec(
                    self.markdown
                )

            if entry.header is MISSING:
                entry.header = HeaderEventSpec()

    async def identify_event_user_as_system(self):
        await self.event_user.identify(
            UserType.SYSTEM, data=dict(type=UserType.SYSTEM)
        )

    def get_quick_replies(self, events: List[Event]) -> List[ButtonEventSpec]:
        all_quick_replies = [
            self.get_quick_replies_from_event(event) for event in events
        ]
        return [
            quick_reply
            for quick_replies in all_quick_replies
            for quick_reply in quick_replies
        ]

    def get_quick_replies_from_event(
        self, event: Event
    ) -> List[ButtonEventSpec]:
        if isinstance(event, InteractiveEvent):
            return event.quick_replies or []
        else:
            return []
