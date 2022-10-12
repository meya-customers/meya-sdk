from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.file.event import FileEvent
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from typing import List
from typing import Optional


@dataclass
class FileComponent(InteractiveComponent):
    """
    Deprecated. Use meya.file.component.v2 instead.
    """

    url: str = element_field(signature=True)
    filename: str = element_field(signature=True)
    icon: Optional[IconElementSpecUnion] = element_field(default=None)
    text: Optional[str] = element_field(default=None)

    async def start(self) -> List[Entry]:
        file_event = FileEvent(
            filename=self.filename,
            icon=IconEventSpec.from_element_spec(self.icon),
            url=self.url,
            text=self.text,
        )
        return self.respond(file_event)
