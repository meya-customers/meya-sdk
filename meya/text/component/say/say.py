from dataclasses import dataclass
from meya.bot.meta_tag import BotOutputTag
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from meya.text.event.say import SayEvent
from typing import List
from typing import Optional
from typing import Type


@dataclass
class SayComponent(InteractiveComponent):
    """
    Send text to the user.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/21-messages-chat-smileys/02-messages-speech-bubbles/messages-bubble-text-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotOutputTag])
    snippet_default: str = meta_field(
        value="""
            say: Hi, nice to meet you!
        """
    )

    say: Optional[str] = element_field(
        signature=True, help="Text to send to the user"
    )

    async def start(self) -> List[Entry]:
        say_event = SayEvent(text=self.say)
        return self.respond(say_event)
