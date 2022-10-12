from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbThemeConfigSpec
from meya.orb.integration.integration import OrbThemeElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbThemeConfig(ThreadConfig[Optional[OrbThemeConfigSpec]]):
    key: ClassVar[str] = "orb_theme"
    type: ClassVar[Type[Optional[OrbThemeConfigSpec]]] = Optional[
        OrbThemeConfigSpec
    ]


@dataclass
class OrbThemeConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbThemeConfig)
    orb_theme: Optional[OrbThemeElementSpec] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_theme is None
            else OrbThemeConfigSpec.from_element_spec(self.orb_theme)
        )
