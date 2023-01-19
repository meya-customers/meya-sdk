from dataclasses import dataclass
from meya.bot.element import BotRef
from meya.bot.meta_tag import BotFlowTag
from meya.component.element import Component
from meya.component.meta_tag import ActionComponentTag
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.icon.spec import IconElementSpecUnion
from typing import List
from typing import Optional
from typing import Type


@dataclass
class FlowComponent(Component):
    """
    This component will start a nested flow (sub-flow).

    https://docs.meya.ai/docs/flows#flow-component

    Here is an example of a flow calling another flow:
    ```yaml
    triggers:
      - keyword: agent

    steps:
      - say: I'll need to get your details first.
      - flow: flow.get_user_info
      - say: Great! Thank you for you info (@ user.name )
      - say: I'll now transfer you to a human agent.
      ...
    ```

    Flow file stored in **flow/get_user_info.yaml**

    ```yaml
    steps:
      - (name)
      - ask: What is your name?
      - user_set: name

      - (email)
      - ask: What is your email address?
      - user_set: email
    ```

    In the above example the first flow calls the flow reference path
    `flow.get_user_info` on the second step. The first flow will then pause
    and wait for the nested flow, `flow.get_user_info`, to complete before
    continuing on to step three.

    ### Flow reference path
    A flow's reference path is simply the **flow's file path** where the
    slashes `/` are replaced with dots `.`, and the file extension is dropped.

    (If you're familiar with Python, a flow reference path is similar to a Python file's module path.)

    Here are some example reference paths:

    - `flow/faq/answers/component.yaml` becomes: `flow.faq.answers.component`
    - `flow/routing.yaml` becomes: `flow.routing`

    ### Flow call stack
    The flow maintains a flow call stack to keep track all the parent flows,
    and where to continue execution from.

    Check the [flow call stack section](https://docs.meya.ai/docs/flows#flow-call-stack) in the
    Flows guide for more info.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/52-arrows-diagrams/02-diagrams/diagram-curve-up-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(
        value=[BotFlowTag, ActionComponentTag]
    )

    flow: FlowRef = element_field(
        signature=True,
        help=(
            "This is the **reference path** to the flow that needs to be "
            "called. A flow's reference path is simply the "
            "**flow's file path** where the slashes `/` are replaced with "
            "dots `.`, and the file extension is dropped. (If you're "
            "familiar with Python, a flow reference path is similar to a "
            "Python files module path)"
        ),
    )
    jump: Optional[StepLabelRef] = element_field(
        default=None,
        help=(
            "This property tells the flow component to jump to a specific "
            "label step in the nested flow. By default, a nested flow will "
            "always start execution from the first step."
        ),
    )
    data: Optional[dict] = element_field(
        default=None,
        help=(
            "This property allows you to pass any flow scope variables from "
            "the calling flow to the nested flow. (This is analogous to "
            "passing function parameters in a conventional programming "
            "language such as Python)."
        ),
    )
    transfer: bool = element_field(
        default=False,
        help=(
            "The property tells the calling flow whether or not to continue "
            "with the flow once the nested flow is complete. If set to "
            "`true`, the bot's flow control will be **transferred** to the "
            "nested flow, and the calling flow will be stopped. The default "
            "is `false`."
        ),
    )
    async_: bool = element_field(
        default=False,
        help=(
            "This property tells the flow component to execute the nested "
            "flow in parallel and continue with the calling flow immediately. "
            "The default is `false`."
        ),
    )
    bot: Optional[BotRef] = element_field(
        default=None,
        help=(
            "The is the **reference path** to the bot that you would like to "
            "run the nested flow for. In Meya you can configure multiple bots "
            "per app and then run flows as different bots. When running a "
            "flow as another bot, any bot events e.g. "
            "[text.say](ref:meya-text-component-say), will be attributed "
            "to that bot with that bot's name and avatar. By default this "
            "property always assumes the primary/default bot if not specified."
        ),
    )
    thread_id: Optional[str] = element_field(
        default=None,
        help=(
            "This property tells the flow component to execute the nested flow "
            "on another conversation thread. This generally used for advanced "
            "use cases where a bot needs to manage multiple conversation "
            "threads."
        ),
    )

    def validate(self):
        super().validate()
        if self.transfer and self.async_:
            raise self.validation_error("transfer is invalid for async flows")
        if self.bot and not self.async_:
            raise self.validation_error("bot is only valid for async flows")
        if self.thread_id and not self.async_:
            raise self.validation_error(
                "thread_id is only valid for async flows"
            )

    async def start(self) -> List[Entry]:
        if self.async_:
            assert self.entry.flow is not None
            return self.flow_control_start_async(
                flow=self.flow,
                label=self.jump,
                data=self.data,
                bot=self.bot,
                thread_id=self.thread_id,
            )
        elif self.transfer:
            assert self.entry.flow is not None
            return self.flow_control_jump_start(
                flow=self.flow, label=self.jump, data=self.data
            )
        else:
            # TODO: Remove redundant "parent_flow" once empty data dict schema is fixed
            return self.flow_control_start(
                flow=self.flow, label=self.jump, data=self.data
            )
