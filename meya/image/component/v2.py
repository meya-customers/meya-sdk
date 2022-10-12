from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.image.event import ImageEvent
from meya.widget.component import WidgetComponent
from typing import List
from typing import Optional


@dataclass
class ImageV2Component(WidgetComponent):
    image: str = element_field(signature=True, help="The URL of the image")
    alt: Optional[str] = element_field(default=None)
    filename: Optional[str] = element_field(default=None)
    text: Optional[str] = element_field(default=None)

    async def build(self) -> List[Entry]:
        image_event = ImageEvent(
            url=self.image,
            filename=self.filename,
            text=self.text,
            alt=self.alt,
        )
        return self.respond(image_event)
