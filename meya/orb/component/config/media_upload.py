from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.orb.integration.integration import OrbMediaUploadConfigSpec
from meya.orb.integration.integration import OrbMediaUploadElementSpec
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class OrbMediaUploadConfig(ThreadConfig[Optional[OrbMediaUploadConfigSpec]]):
    key: ClassVar[str] = "orb_media_upload"
    type: ClassVar[Type[Optional[OrbMediaUploadConfigSpec]]] = Optional[
        OrbMediaUploadConfigSpec
    ]


@dataclass
class OrbMediaUploadConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=OrbMediaUploadConfig)
    orb_media_upload: Optional[OrbMediaUploadElementSpec] = element_field(
        signature=True
    )

    def get_component_value(self) -> Any:
        return (
            None
            if self.orb_media_upload is None
            else OrbMediaUploadConfigSpec.from_element_spec(
                self.orb_media_upload
            )
        )
