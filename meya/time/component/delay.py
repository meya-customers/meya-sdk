import asyncio

from dataclasses import dataclass
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from meya.text.event.say import SayEvent
from meya.time.meta_tag import TimeTag
from numbers import Real
from typing import List
from typing import Type

MAX_DELAY: Real = 20


@dataclass
class DelayComponent(Component):
    """
    Pause flow execution for a short time.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/18-time/hourglass-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotFlowTag, TimeTag])

    delay: Real = element_field(signature=True, help="Delay seconds")

    def validate(self):
        super().validate()
        if self.delay > MAX_DELAY:
            raise self.validation_error(
                f"delay cannot be longer than {MAX_DELAY} seconds"
            )

    async def start(self) -> List[Entry]:
        if self.thread.voice is None:
            await asyncio.sleep(float(self.delay))
            return self.respond()
        else:
            # In the voice case we use SSML for client side delays instead of
            # server side delays to prevent the voice integration request from
            # timing out
            say_event = SayEvent(
                text=f'<break time="{int(self.delay * 1000)}ms"/>'
            )
            return self.respond(say_event)
