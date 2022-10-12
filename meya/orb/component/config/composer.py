from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbComposerConfigSpec
from meya.orb.integration.integration import OrbComposerElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbComposerConfig(ThreadConfig[Optional[OrbComposerConfigSpec]]):
    key: ClassVar[str] = "orb_composer"
    type: ClassVar[Type[Optional[OrbComposerConfigSpec]]] = Optional[
        OrbComposerConfigSpec
    ]


@dataclass
class OrbComposerConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbComposerConfig)
    orb_composer: Optional[OrbComposerElementSpec] = element_field(
        signature=True
    )

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_composer is None
            else OrbComposerConfigSpec.from_element_spec(self.orb_composer)
        )
