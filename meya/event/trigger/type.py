from dataclasses import dataclass
from meya.element.field import element_field
from meya.event.entry import Event
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Any


@dataclass
class TypeTrigger(Trigger):
    event_type: str = element_field(signature=True)
    when: Any = element_field(default=True)

    def validate(self):
        entry_subclass = Event.try_get_entry_type_subclass(self.event_type)
        if not entry_subclass:
            raise self.validation_error(
                f'invalid event type "{self.event_type}"'
            )

    async def match(self) -> TriggerMatchResult:
        if self.entry.get_entry_type() == self.event_type:
            return self.succeed()
        else:
            return self.fail()
