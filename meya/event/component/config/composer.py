from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.event.component.config.event import EventConfig
from meya.event.component.config.event import EventConfigComponent
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerEventSpec
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class ComposerConfig(EventConfig[Optional[ComposerEventSpec]]):
    key: ClassVar[str] = "event_composer"
    type: ClassVar[Optional[ComposerEventSpec]] = Optional[ComposerEventSpec]


@dataclass
class ComposerConfigComponent(EventConfigComponent):
    config: Type[EventConfig] = meta_field(value=ComposerConfig)
    composer: Optional[ComposerElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        if self.composer is None:
            return None
        else:
            return ComposerEventSpec.from_element_spec(self.composer)
