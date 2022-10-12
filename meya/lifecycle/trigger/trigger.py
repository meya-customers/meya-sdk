from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.lifecycle.event.event import LifecycleEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class LifecycleTrigger(Trigger):
    @dataclass
    class Response:
        context: Dict[str, Any] = response_field(sensitive=True)

    meta_level: float = meta_field(value=MetaLevel.BASIC)

    lifecycle_id: str = element_field(signature=True)
    text: Optional[str] = element_field(default=None)
    when: Any = element_field(default=True)

    entry: LifecycleEvent = process_field()
    encrypted_entry: LifecycleEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        if self.lifecycle_id != self.entry.lifecycle_id:
            return self.fail()
        else:
            return self.succeed(
                data=LifecycleTrigger.Response(
                    context=self.encrypted_entry.context
                )
            )
