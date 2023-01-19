from dataclasses import dataclass
from meya.bot.meta_tag import BotOutputTag
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from meya.text.event.say import SayEvent
from typing import List
from typing import Optional
from typing import Type


@dataclass
class SayComponent(InteractiveComponent):
    """
    Send text to the user. This is the most used and simplest output component
    in the Meya SDK. It simply takes a text string and creates a [text.say](ref:meya-text-event-say)
    event that then gets displayed to the user.

    ```yaml
    - say: Hello world!
    ```

    Which produces the following in the [Meya Orb Web SDK](https://docs.meya.ai/docs/orb-web-sdk) client:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-say.png" width="400"/>

    Although the `say` component is very simple to use, it is also an interactive
    component which allows you to set [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies), configure the
    [input composer](https://docs.meya.ai/docs/composer), configure the [markdown support](https://docs.meya.ai/docs/markdown), set context data and attach
    [component triggers](https://docs.meya.ai/docs/component-triggers).

    Here is a more advanced example:

    ```yaml
    - say: Hello **world**! https://en.wikipedia.org/wiki/%22Hello,_World!%22_program
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
        focus: blur
        visibility: collapse
        collapse_placeholder: Click to start typing
      markdown:
        - format
        - linkify
    ```

    Which produces the following output:

    <img src="https://cdn.meya.ai/docs/images/meya-text-component-say-1.png" width="400"/>

    **Note**, not all integrations support the **quick_replies**, **composer** and **markdown**
    fields. Check the [compatibility matrix](https://docs.meya.ai/docs/card-compatibility-matrix)
    and integration documentation to see which features the specific integration
    you are using supports.

    ### Advanced use-case

    You can even use **component triggers** to allow the say component to wait
    and capture user input, which effectively turns this into an input component.

    ```yaml
    - say: What's your name?
      triggers:
        - catchall
    ```

    Because of the `catchall` trigger, the bot will wait for user input and store
    the value in `(@ flow.result )`. Check the [component triggers guide](https://docs.meya.ai/docs/component-triggers)
    for more info.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/21-messages-chat-smileys/02-messages-speech-bubbles/messages-bubble-text-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[BotOutputTag])
    snippet_default: str = meta_field(
        value="""
            say: Hi, nice to meet you!
        """
    )

    say: Optional[str] = element_field(
        signature=True, help="Text to send to the user."
    )

    async def start(self) -> List[Entry]:
        say_event = SayEvent(text=self.say)
        return self.respond(say_event)
