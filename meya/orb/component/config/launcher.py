from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbLauncherConfigSpec
from meya.orb.integration.integration import OrbLauncherElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbLauncherConfig(ThreadConfig[Optional[OrbLauncherConfigSpec]]):
    key: ClassVar[str] = "orb_launcher"
    type: ClassVar[Type[Optional[OrbLauncherConfigSpec]]] = Optional[
        OrbLauncherConfigSpec
    ]


@dataclass
class OrbLauncherConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbLauncherConfig)
    orb_launcher: Optional[OrbLauncherElementSpec] = element_field(
        signature=True
    )

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_launcher is None
            else OrbLauncherConfigSpec.from_element_spec(self.orb_launcher)
        )
