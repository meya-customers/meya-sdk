from dataclasses import MISSING
from dataclasses import dataclass
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry.interactive import InteractiveEvent
from meya.event.header_spec import HeaderElementSpec
from meya.event.header_spec import HeaderEventSpec
from meya.text.markdown import MarkdownElementSpecUnion
from meya.text.markdown import MarkdownEventSpecHelper
from typing import List
from typing import Optional


@dataclass
class InteractiveComponent(Component):
    is_abstract: bool = meta_field(value=True)

    quick_replies: List[ButtonElementSpecUnion] = element_field(
        default_factory=list,
        snippet_default="""
            - text: Yes
              action: next
            - text: No
              action: next
        """,
        help="List of buttons that the user can select for replies",
        level=MetaLevel.VERY_BASIC,
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        help="Override the Orb composer for this component",
        level=MetaLevel.ADVANCED,
    )
    header: HeaderElementSpec = element_field(
        default_factory=HeaderElementSpec,
        help="Override the header for this component",
        level=MetaLevel.ADVANCED,
    )
    markdown: Optional[MarkdownElementSpecUnion] = element_field(
        default=None,
        help="Override the bot Markdown mode for this component",
        level=MetaLevel.ADVANCED,
    )

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        super().post_process(entry, extra_entries)

        if isinstance(entry, InteractiveEvent):
            if entry.quick_replies is MISSING:
                (
                    quick_replies,
                    quick_reply_triggers,
                ) = ButtonEventSpec.from_element_spec_union_list(
                    self.quick_replies, skip_triggers=self.skip_triggers
                )
                entry.quick_replies = quick_replies
                extra_entries.extend(quick_reply_triggers)

            if entry.composer is MISSING:
                from meya.event.component.config.composer import ComposerConfig

                entry.composer = ComposerEventSpec.from_element_spec(
                    self.composer
                ) | (ComposerConfig.get() or ComposerEventSpec())

            if entry.header is MISSING:
                from meya.event.component.config.header import HeaderConfig

                header, header_triggers = HeaderEventSpec.from_element_spec(
                    self.header, skip_triggers=self.skip_triggers
                )
                entry.header = header | (
                    HeaderConfig.get() or HeaderEventSpec()
                )
                extra_entries.extend(header_triggers)

            if entry.markdown is MISSING and self.markdown is not None:
                entry.markdown = MarkdownEventSpecHelper.from_element_spec(
                    self.markdown
                )
