from dataclasses import dataclass
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.image.event import ImageEvent
from meya.media.trigger import MediaTrigger


@dataclass
class ImageTrigger(MediaTrigger):
    """
    Match when an image is uploaded by a user.

    When the trigger matches, the image file's URL is saved in the
    `(@ flow.result )` [flow scope](https://docs.meya.ai/docs/scope#flow)
    variable.

    This trigger also has a BFML alias that allows you to reference the
    trigger using the `image` word.

    ```yaml
    triggers:
      - image
    steps:
      - say: "Uploaded image file: (@ flow.result )"
    ```
    """

    extra_alias: str = meta_field(value="image")

    entry: ImageEvent = process_field()
    encrypted_entry: ImageEvent = process_field()
