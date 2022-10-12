from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbMenuConfigSpec
from meya.orb.integration.integration import OrbMenuElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbMenuConfig(ThreadConfig[Optional[OrbMenuConfigSpec]]):
    key: ClassVar[str] = "orb_menu"
    type: ClassVar[Type[Optional[OrbMenuConfigSpec]]] = Optional[
        OrbMenuConfigSpec
    ]


@dataclass
class OrbMenuConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbMenuConfig)
    orb_menu: Optional[OrbMenuElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_menu is None
            else OrbMenuConfigSpec.from_element_spec(self.orb_menu)
        )
