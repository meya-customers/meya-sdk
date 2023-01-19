from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.text.event.status import StatusEvent
from typing import List


@dataclass
class StatusComponent(InteractiveComponent):
    """
    Displays a simple status message to the user.

    ```yaml
    - status: Bot status message!
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-status.png" width="400"/>

    By default, the status message will always appear in the chat history, however,
    sometimes you would like to only display the status message temporarily. In
    this case you can make the status ephemeral and the status message will
    disappear when another bot event appears.

    Example of an ephemeral status message:

    ```yaml
    - status: Bot status message!
      ephemeral: true
    ```
    """

    status: str = element_field(
        signature=True, help="Text to display to the user."
    )
    ephemeral: bool = element_field(
        default=False,
        help=(
            "Hide the status message when a new event arrives. If set to "
            "`false`, then the status message will remain visible in the "
            "conversation history."
        ),
    )

    async def start(self) -> List[Entry]:
        status_event = StatusEvent(
            status=self.status, ephemeral=self.ephemeral
        )
        return self.respond(status_event)
