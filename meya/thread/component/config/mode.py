from dataclasses import dataclass
from meya.db.view.thread import ThreadMode
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.thread.component.config.config import ThreadConfig
from meya.thread.component.config.config import ThreadConfigComponent
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class ThreadModeConfig(ThreadConfig[ThreadMode]):
    key: ClassVar[str] = "mode"
    type: ClassVar[Type[ThreadMode]] = ThreadMode


@dataclass
class ThreadModeConfigComponent(ThreadConfigComponent):
    config: Type[ThreadConfig] = meta_field(value=ThreadModeConfig)
    mode: Optional[ThreadMode] = element_field(signature=True)

    def get_component_value(self) -> Any:
        return ThreadMode(self.mode)
