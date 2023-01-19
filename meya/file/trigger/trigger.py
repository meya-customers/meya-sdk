from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.file.event import FileEvent
from meya.media.trigger import MediaTrigger


@dataclass
class FileTrigger(MediaTrigger):
    """
    Match when a file is uploaded by a user.

    When the trigger matches, the file's URL is saved in the
    `(@ flow.result )` [flow scope](https://docs.meya.ai/docs/scope#flow)
    variable.

    This trigger also has a BFML alias that allows you to reference the
    trigger using the `file` word.

    ```yaml
    triggers:
      - file
    steps:
      - say: "Uploaded file: (@ flow.result )"
    ```
    """

    extra_alias: str = meta_field(value="file")

    entry: FileEvent = process_field()
    encrypted_entry: FileEvent = process_field()
