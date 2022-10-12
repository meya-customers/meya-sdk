from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbDropConfigSpec
from meya.orb.integration.integration import OrbDropElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbDropConfig(ThreadConfig[Optional[OrbDropConfigSpec]]):
    key: ClassVar[str] = "orb_drop"
    type: ClassVar[Type[Optional[OrbDropConfigSpec]]] = Optional[
        OrbDropConfigSpec
    ]


@dataclass
class OrbDropConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbDropConfig)
    orb_drop: Optional[OrbDropElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_drop is None
            else OrbDropConfigSpec.from_element_spec(self.orb_drop)
        )
