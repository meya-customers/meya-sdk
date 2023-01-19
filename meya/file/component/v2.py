from dataclasses import dataclass
from meya.element.field import element_field
from meya.entry import Entry
from meya.file.event import FileEvent
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.widget.component.component import WidgetComponent
from typing import List
from typing import Optional


@dataclass
class FileV2Component(WidgetComponent):
    """
    Display a file to the user that the user can click and download. This
    component can be used as a normal component in a flow step, or as a field
    with in a page component.

    ```yaml
    - file: https://upload.wikimedia.org/wikipedia/commons/b/b3/Wiki_markup_cheatsheet_EN.pdf
      name: cheatsheet.pdf
      icon: streamline-regular/07-work-office-companies/07-office-files/office-file-pdf-1.svg
      text: Wikipedia markup cheatsheet
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-file-component-v2.png" width="400"/>

    The file component is also an interactive component which allows you to set
    [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown),
    set context data and attach [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - file: https://upload.wikimedia.org/wikipedia/commons/b/b3/Wiki_markup_cheatsheet_EN.pdf
      name: cheatsheet.pdf
      icon: streamline-regular/07-work-office-companies/07-office-files/office-file-pdf-1.svg
      text: Wikipedia **markup cheatsheet**
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
        focus: file
      markdown:
        - format
        - linkify
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-file-component-v2-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies**, **composer** and **markdown**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Pages support
    This file component is also a widget component that can be displayed as a field
    in a page.

    Here is an example using the regex input component in a page:

    ```yaml
    - page:
      - file: https://upload.wikimedia.org/wikipedia/commons/b/b3/Wiki_markup_cheatsheet_EN.pdf
        name: cheatsheet.pdf
        icon: streamline-regular/07-work-office-companies/07-office-files/office-file-pdf-1.svg
        text: Wikipedia markup cheatsheet
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-file-component-v2-page.png" width="400"/>

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input.
    """

    file: str = element_field(signature=True, help="The URL of the file.")
    name: str = element_field(help="The file's file name and extension.")
    icon: Optional[IconElementSpecUnion] = element_field(
        default=None,
        help=(
            "The icon spec or URL to use for the file. See the "
            "[Icons](https://docs.meya.ai/docs/icons) guide for more info."
        ),
    )
    text: Optional[str] = element_field(
        default=None,
    )

    async def build(self) -> List[Entry]:
        file_event = FileEvent(
            filename=self.name,
            icon=IconEventSpec.from_element_spec(self.icon),
            url=self.file,
            text=self.text,
        )
        return self.respond(file_event)
