from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.file.event import FileEvent
from meya.media.trigger import MediaTrigger


@dataclass
class FileTrigger(MediaTrigger):
    extra_alias: str = meta_field(value="file")

    entry: FileEvent = process_field()
    encrypted_entry: FileEvent = process_field()
