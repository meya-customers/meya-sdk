from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.image.event import ImageEvent
from meya.widget.component import WidgetComponent
from typing import List
from typing import Optional


@dataclass
class ImageV2Component(WidgetComponent):
    """
    Display an image to the user. This component can be used as a normal
    component in a flow step, or as a field with in a page component.

    ```yaml
    - image: https://images.unsplash.com/photo-1476610182048-b716b8518aae?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1000
      alt: Photo of a landscape and waterfall
      text: Photo of a landscape and waterfall
      filename: landscape_photo.jpg
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-image-component-v2.png" width="400"/>

    The image component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown),
    set context data and attach [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - image: https://images.unsplash.com/photo-1476610182048-b716b8518aae?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1000
      alt: Photo of a landscape and waterfall
      text: Photo of a landscape and waterfall
      filename: landscape_photo.jpg
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
        focus: text
        placeholder: Type your name here
      markdown:
        - format
        - linkify
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-image-component-v2-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies**, **composer** and **markdown**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Pages support
    This image component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the regex input component in a page:

    ```yaml
    - page:
      - image: https://images.unsplash.com/photo-1476610182048-b716b8518aae?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1000
        alt: Photo of a landscape and waterfall
        text: Photo of a landscape and waterfall
        filename: landscape_photo.jpg
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-image-component-v2-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    image: str = element_field(signature=True, help="The URL of the image.")
    alt: Optional[str] = element_field(
        default=None,
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

    async def build(self) -> List[Entry]:
        image_event = ImageEvent(
            url=self.image,
            filename=self.filename,
            text=self.text,
            alt=self.alt,
        )
        return self.respond(image_event)
