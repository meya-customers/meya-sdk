from dataclasses import dataclass
from meya.db.view.thread import ThreadMode
from meya.db.view.user import UserType
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.media.event import MediaEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from meya.trigger.element import TriggerResponse


@dataclass
class MediaTrigger(Trigger):
    """
    Match when a media file is uploaded by a user.

    When the trigger matches, the media file's URL is saved in the
    `(@ flow.result )` [flow scope](https://docs.meya.ai/docs/scope#flow)
    variable.

    This trigger also has a BFML alias that allows you to reference the
    trigger using the `media` word.

    ```yaml
    triggers:
      - media
    steps:
      - say: "Uploaded file: (@ flow.result )"
    ```
    """

    extra_alias: str = meta_field(value="media")

    entry: MediaEvent = process_field()
    encrypted_entry: MediaEvent = process_field()

    async def default_when(self) -> bool:
        if self.event_user.type != UserType.USER:
            return False
        if self.thread.mode == ThreadMode.BOT:
            return True
        else:
            return False

    async def match(self) -> TriggerMatchResult:
        return self.succeed(
            data=TriggerResponse(result=self.encrypted_entry.url)
        )
