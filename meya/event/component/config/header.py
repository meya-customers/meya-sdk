from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.event.component.config.event import EventConfig
from meya.event.component.config.event import EventConfigComponent
from meya.event.header_spec import HeaderElementSpec
from meya.event.header_spec import HeaderEventSpec
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class HeaderConfig(EventConfig[Optional[HeaderEventSpec]]):
    key: ClassVar[str] = "event_header"
    type: ClassVar[Optional[HeaderEventSpec]] = Optional[HeaderEventSpec]


@dataclass
class HeaderConfigComponent(EventConfigComponent):
    config: Type[EventConfig] = meta_field(value=HeaderConfig)
    header: Optional[HeaderElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.header is None
            else HeaderEventSpec.from_element_spec(
                self.header, skip_triggers=True
            )[0]
        )
