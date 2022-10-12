from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbHeaderConfigSpec
from meya.orb.integration.integration import OrbHeaderElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbHeaderConfig(ThreadConfig[Optional[OrbHeaderConfigSpec]]):
    key: ClassVar[str] = "orb_header"
    type: ClassVar[Type[Optional[OrbHeaderConfigSpec]]] = Optional[
        OrbHeaderConfigSpec
    ]


@dataclass
class OrbHeaderConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbHeaderConfig)
    orb_header: Optional[OrbHeaderElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_header is None
            else OrbHeaderConfigSpec.from_element_spec(
                self.orb_header, skip_triggers=True
            )[0]
        )
