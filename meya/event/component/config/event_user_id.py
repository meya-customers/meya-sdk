from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.event.component.config.event import EventConfig
from meya.event.component.config.event import EventConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class EventUserIdConfig(EventConfig[Optional[str]]):
    key: ClassVar[str] = "event_user_id"
    type: ClassVar[Optional[str]] = Optional[str]


@dataclass
class EventUserIdConfigComponent(EventConfigComponent):
    config: Type[EventConfig] = meta_field(value=EventUserIdConfig)
    event_user_id: Optional[str] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return self.event_user_id
