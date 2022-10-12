from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.text.event import TextEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from numbers import Real
from typing import Any


@dataclass
class TextTriggerResponse:
    result: str = response_field(sensitive=True)


@dataclass
class TextTrigger(Trigger):
    is_abstract: bool = meta_field(value=True)

    entry: TextEvent = process_field()
    encrypted_entry: TextEvent = process_field()

    async def accept(self) -> bool:
        if not await super().accept():
            return False
        return bool(self.entry.text)

    def succeed(
        self, *, confidence: Real = Trigger.MAX_CONFIDENCE, data: Any = None
    ) -> TriggerMatchResult:
        return super().succeed(
            confidence=confidence,
            data=TextTriggerResponse(result=self.encrypted_entry.text)
            if data is None
            else data,
        )
