from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.event.component.config.event import EventConfig
from meya.event.component.config.event import EventConfigComponent
from meya.text.markdown import MarkdownElementSpecUnion
from meya.text.markdown import MarkdownEventSpec
from meya.text.markdown import MarkdownEventSpecHelper
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type


class MarkdownConfig(EventConfig[Optional[MarkdownEventSpec]]):
    key: ClassVar[str] = "event_markdown"
    type: ClassVar[Optional[MarkdownEventSpec]] = Optional[MarkdownEventSpec]


@dataclass
class MarkdownConfigComponent(EventConfigComponent):
    config: Type[EventConfig] = meta_field(value=MarkdownConfig)
    markdown: Optional[MarkdownElementSpecUnion] = element_field(
        signature=True
    )

    def get_component_value(self) -> Any:
        if self.markdown is None:
            return None
        else:
            return MarkdownEventSpecHelper.from_element_spec(self.markdown)
