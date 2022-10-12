from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.image.event import ImageEvent
from typing import List
from typing import Optional


@dataclass
class ImageComponent(InteractiveComponent):
    """
    Deprecated. Use meya.image.component.v2 instead.
    """

    url: str = element_field(signature=True)
    alt: str = element_field(signature=True)
    filename: Optional[str] = element_field(default=None)
    text: Optional[str] = element_field(default=None)

    async def start(self) -> List[Entry]:
        image_event = ImageEvent(
            url=self.url, filename=self.filename, text=self.text, alt=self.alt
        )
        return self.respond(image_event)
