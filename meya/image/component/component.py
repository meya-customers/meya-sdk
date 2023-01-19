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
    `DEPRECATED`

     Use [image.v2](https://docs.meya.ai/reference/meya-image-component-v2) instead.
    """

    url: str = element_field(signature=True, help="The URL of the image.")
    alt: str = element_field(
        signature=True,
        help=(
            "The image's alternative text. This text is displayed if the "
            "image could not be loaded."
        ),
    )
    filename: Optional[str] = element_field(
        default=None, help="The image's file name."
    )
    text: Optional[str] = element_field(
        default=None, help="Text to be displayed along with the image."
    )

    async def start(self) -> List[Entry]:
        image_event = ImageEvent(
            url=self.url, filename=self.filename, text=self.text, alt=self.alt
        )
        return self.respond(image_event)
