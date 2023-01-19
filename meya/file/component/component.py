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
    `DEPRECATED`

     Use [file.v2](https://docs.meya.ai/reference/meya-file-component-v2) instead.
    """

    url: str = element_field(signature=True, help="The URL of the file.")
    filename: str = element_field(
        signature=True, help="The file's file name and extension."
    )
    icon: Optional[IconElementSpecUnion] = element_field(
        default=None,
        help=(
            "The icon spec or URL to use for the file. See the "
            "[Icons](https://docs.meya.ai/docs/icons) guide for more info."
        ),
    )
    text: Optional[str] = element_field(
        default=None, help="Text to be displayed along with the file."
    )

    async def start(self) -> List[Entry]:
        file_event = FileEvent(
            filename=self.filename,
            icon=IconEventSpec.from_element_spec(self.icon),
            url=self.url,
            text=self.text,
        )
        return self.respond(file_event)
