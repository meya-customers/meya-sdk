from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.image.event import ImageEvent
from meya.media.trigger import MediaTrigger


@dataclass
class ImageTrigger(MediaTrigger):
    extra_alias: str = meta_field(value="image")

    entry: ImageEvent = process_field()
    encrypted_entry: ImageEvent = process_field()
