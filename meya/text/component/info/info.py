from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.text.event.info import InfoEvent
from meya.widget.component import WidgetComponent
from typing import List


@dataclass
class InfoComponent(WidgetComponent):
    """
    Displays a block of plain text without any speech bubble framing.

    ```yaml
    - info: |
        # Example info

        This is some example info text.
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-info.png" width="400"/>

    The info component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown),
    set context data and attach [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - info: |
        # Example info

        This is some example info text.
      quick_replies:
        - text: Discover earth
        - text: Talk to an agent
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

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-info-1.png" width="400"/>

    **Note**, this component is only compatible with the
    [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk)
    and [Meya Orb Mobile SDK](https://docs.meya.ai/docs/orb-mobile-sdk).

    ### Pages support
    This info component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the info component in a page:

    ```yaml
    - page:
      - info: |
          # Example info

          This is some example info text.
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-info-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    info: str = element_field(
        signature=True,
        help=(
            "The text to display in the info block. This field also supports "
            "markdown."
        ),
    )

    async def build(self) -> List[Entry]:
        event = InfoEvent(info=self.info)
        return self.respond(event)
