from dataclasses import dataclass
from dataclasses import field
from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.icon.spec import IconElementSpecUnion
from meya.text.event.ask import AskEvent
from meya.text.trigger.catchall import CatchallTrigger
from meya.text.trigger.trigger import TextTriggerResponse
from meya.trigger.element import Trigger
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.user.meta_tag import UserInputTag
from meya.util.dict import from_dict
from numbers import Real
from typing import Any
from typing import List
from typing import Optional
from typing import Type


class AskValidationError(Exception):
    pass


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.TEXT)
    visibility: Optional[ComposerVisibility] = field(
        default=ComposerVisibility.SHOW
    )


@dataclass
class AskComponent(InteractiveComponent):
    """
    Get basic text input from the user.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/21-messages-chat-smileys/02-messages-speech-bubbles/messages-bubble-question.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])
    snippet_default: str = meta_field(
        value="""
            ask: What's your name?
        """
    )

    ask: Optional[str] = element_field(
        signature=True, help="Question to send to the user"
    )
    retries: Real = element_field(default=float("inf"), level=MetaLevel.HIDDEN)
    error_message: str = element_field(
        default="Invalid input, please try again.", level=MetaLevel.HIDDEN
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    async def start(self) -> List[Entry]:
        self.reset()
        return self._ask(self.ask)

    async def next(self) -> List[Entry]:
        try:
            response = await self.next_response()
            return self.respond(data=response)
        except AskValidationError:
            encrypted_response = from_dict(
                TextTriggerResponse, self.entry.data
            )
            input_result = ComponentErrorResponse(
                result=encrypted_response.result,
                retry_count=self.entry.data.get(
                    AskComponent.RETRY_COUNT_KEY, 0
                ),
            )
            if input_result.retry_count >= self.retries:
                return self.respond(data=input_result)
            else:
                input_result.retry_count += 1
                return self._ask(self.error_message, data=input_result)

    def _ask(self, text: str, *, data: Any = None) -> List[Entry]:
        ask_event = AskEvent(text=text)
        return self.respond(ask_event, self.trigger(data))

    def trigger(self, data: Any = None) -> TriggerActivateEntry:
        return CatchallTrigger(
            action=self.get_next_action(data=data),
            confidence=Trigger.MAX_CONFIDENCE,
        ).activate()

    async def next_response(self) -> Any:
        encrypted_response = from_dict(TextTriggerResponse, self.entry.data)
        return ComponentOkResponse(result=encrypted_response.result)
