from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.file.event import FileEvent
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.widget.component.component import WidgetComponent
from typing import List
from typing import Optional


@dataclass
class FileV2Component(WidgetComponent):
    file: str = element_field(signature=True, help="The URL of the file")
    name: str = element_field()
    icon: Optional[IconElementSpecUnion] = element_field(default=None)
    text: Optional[str] = element_field(default=None)

    async def build(self) -> List[Entry]:
        file_event = FileEvent(
            filename=self.name,
            icon=IconEventSpec.from_element_spec(self.icon),
            url=self.file,
            text=self.text,
        )
        return self.respond(file_event)
