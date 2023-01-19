from dataclasses import dataclass
from dataclasses import field
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.image.trigger import ImageTrigger
from meya.text.event.ask import AskEvent
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.IMAGE)
    visibility: Optional[ComposerVisibility] = field(
        default=ComposerVisibility.SHOW
    )


class Expect(SimpleEnum):
    IMAGE = "image"


@dataclass
class ImageAskComponent(InteractiveComponent):
    """
    Ask the user to upload an image. This will store the image in the Meya
    blob storage, and encrypt the image if [Sensitive Data](https://docs.meya.ai/docs/sensitive-data)
    has been enabled.

    ```yaml
    - ask: Please upload a photo
      expect: image
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-image-component-ask.png" width="400"/>

    **Note**, by default this component will show the **File** and **Photo**
    upload buttons in the Orb's input composer.

    The ask image component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown),
    set context data and attach [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - ask: Please upload a **photo**
      expect: image
      quick_replies:
        - text: Discover earth
          action:
            flow: flow.earth
        - text: Talk to an agent
          action:
            flow: flow.agent
      context:
        foo: bar
      composer:
        focus: image
      markdown:
        - format
        - linkify
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-image-component-ask-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies**, **composer** and **markdown**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Input validation

    The ask image component does not do any file type or extension checking on the
    uploaded file. All it expects is a valid [image](https://docs.meya.ai/reference/meya-image-event)
    event. The **image** event will be created by the specific integration that
    the user is using e.g. Orb, WhatsApp etc. and each integration will do some
    basic file type and/or MIME type checking before it creates and publishes
    the **image** event.
    """

    ask: Optional[str] = element_field(
        signature=True, help="Question to send to the user."
    )
    expect: Optional[Expect] = element_field(
        signature=True,
        default=None,
        help="The type of input to expect, `image`.",
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help=(
            "The composer spec that allows you to control the Orb's input "
            "composer. Check the "
            "[Composer](https://docs.meya.ai/docs/composer) guide for more "
            "info."
        ),
    )

    async def start(self) -> List[Entry]:
        ask_event = AskEvent(text=self.ask)

        return self.respond(
            ask_event, ImageTrigger(action=self.get_next_action()).activate()
        )
