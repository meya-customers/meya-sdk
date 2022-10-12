from dataclasses import MISSING
from dataclasses import dataclass
from meya.bot.element.integration import default_bot_integration
from meya.bot.entry import BotEntry
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserView
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.entry import Entry
from meya.event.composer_spec import ComposerEventSpec
from meya.event.entry import Event
from meya.event.entry.interactive import InteractiveEvent
from meya.event.header_spec import HeaderEventSpec
from meya.icon.spec import IconElementSpecUnion
from meya.presence.event.typing.typing import TypingEvent
from meya.text.markdown import MarkdownElementSpecUnion
from meya.text.markdown import MarkdownEventSpecHelper
from meya.util.avatar import Avatar
from meya.util.context_var import ScopedContextVar
from typing import ClassVar
from typing import List
from typing import Type
from typing import Union
from typing import cast


@dataclass
class BotAvatar(Avatar):
    pass


@dataclass
class Bot(Element):
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/02-technology/01-artificial-intelligence/robot-head-1.svg"
    )

    name: str = element_field(default="Bot")
    avatar: BotAvatar = element_field(default_factory=BotAvatar)
    markdown: MarkdownElementSpecUnion = element_field(default=False)
    typing: bool = element_field(
        default=True,
        help=(
            "When set to 'False', all typing indicators emitted by the bot "
            "via the 'typing' component will be ignored and not sent to "
            "any connected integrations."
        ),
    )
    default: bool = element_field(default=True)
    entry: Union[BotEntry, Event] = process_field()

    bot_user: UserView = process_field()

    current: ClassVar = cast(ScopedContextVar["Bot"], ScopedContextVar())

    def __post_init__(self):
        super().__post_init__()
        self.bot_user = UserView()

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

        if isinstance(entry, BotEntry):
            if entry.bot_id is MISSING and self.id:
                entry.bot_id = self.id

            if entry.thread_id is MISSING and self.thread.id:
                entry.thread_id = self.thread.id

        if isinstance(entry, Event):
            if entry.user_id is MISSING and self.event_user.id:
                entry.user_id = self.event_user.id

            if entry.thread_id is MISSING and self.thread.id:
                entry.thread_id = self.thread.id

            if entry.integration_id is MISSING:
                entry.integration_id = default_bot_integration.id

            if entry.context is MISSING:
                entry.context = {}

            if not entry.sensitive and self.thread.mode != ThreadMode.BOT:
                entry.sensitive = True

        if isinstance(entry, InteractiveEvent):
            if entry.quick_replies is MISSING:
                entry.quick_replies = []

            if entry.composer is MISSING:
                from meya.event.component.config.composer import ComposerConfig

                entry.composer = ComposerConfig.get() or ComposerEventSpec()

            if entry.header is MISSING:
                from meya.event.component.config.header import HeaderConfig

                entry.header = HeaderConfig.get() or HeaderEventSpec()

            if entry.markdown is MISSING:
                from meya.event.component.config.markdown import MarkdownConfig

                markdown = MarkdownConfig.get()
                entry.markdown = (
                    markdown
                    if markdown is not None
                    else MarkdownEventSpecHelper.from_element_spec(
                        self.markdown
                    )
                )

    @classmethod
    def get_current_id(cls) -> str:
        return cls.current.get().id


class BotSpec(Spec):
    element_type: ClassVar[Type[Element]] = Bot


class BotRef(Ref):
    element_type: ClassVar[Type[Element]] = Bot
