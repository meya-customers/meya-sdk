from dataclasses import dataclass
from meya.button.event.click import ButtonClickEvent
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class ButtonTrigger(Trigger):
    """
    Match a statically defined button ID in a button click event.

    ```yaml
    - button_id: agent_escalation
      when: true
    ```

    This will match any [button.click](https://docs.meya.ai/reference/meya-button-event-click) event where
    the button ID is set to `agent_escalation`.

    You can define a static button ID as follows:

    ```yaml
    steps:
      - say: How can I help you?
        quick_replies:
          - text: Questions about credit cards
            action:
                flow: flow.credit_cards
          - text: Talk to an agent
            button_id: agent_escalation
    ```

    When the user clicks the `Talk to an agent` quick reply, it will create
    new [button.click](https://docs.meya.ai/reference/meya-button-event-click) event with the button ID
    set as `agent_escalation`. This will then match the button trigger above.

    Note, that the trigger's `when` field is set to `true`, which means tha the
    trigger will always evaluate, event when the conversation thread's mode isn't
    `bot`. Check the [when section](https://docs.meya.ai/docs/triggers-1#when) in the triggers guide
    for more info on when triggers are evaluated.

    Check the [triggers guide](https://docs.meya.ai/docs/triggers-1#button_id-trigger) for extra info.

    """

    @dataclass
    class Response:
        context: Dict[str, Any] = response_field()

    button_id: str = element_field(
        signature=True,
        help=(
            "The static button ID to match against. Use this button ID in the "
            "`button_id` field in the relevant quick replies and buttons."
        ),
    )
    text: Optional[str] = element_field(default=None, help="`DEPRECATED`")
    when: Any = element_field(
        default=True,
        help=(
            "Optionally set the criteria when this trigger should evaluate. "
            "The default is `true` and will always evaluate."
        ),
    )

    entry: ButtonClickEvent = process_field()
    encrypted_entry: ButtonClickEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        if self.button_id != self.entry.button_id:
            return self.fail()
        else:
            return self.succeed(
                data=ButtonTrigger.Response(
                    context=self.encrypted_entry.context
                )
            )
