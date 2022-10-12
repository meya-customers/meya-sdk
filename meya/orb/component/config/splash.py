from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbSplashConfigSpec
from meya.orb.integration.integration import OrbSplashElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbSplashConfig(ThreadConfig[Optional[OrbSplashConfigSpec]]):
    key: ClassVar[str] = "orb_splash"
    type: ClassVar[Type[Optional[OrbSplashConfigSpec]]] = Optional[
        OrbSplashConfigSpec
    ]


@dataclass
class OrbSplashConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbSplashConfig)
    orb_splash: Optional[OrbSplashElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_splash is None
            else OrbSplashConfigSpec.from_element_spec(self.orb_splash)
        )
