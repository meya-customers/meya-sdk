from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.text.component.ask import AskComponent
from meya.trigger.element import Trigger
from numbers import Real
from typing import Optional


@dataclass
class AskCatchallComponent(AskComponent):
    """
    This is an abstract component and is used by the following components:

    - [email.address.ask](https://docs.meya.ai/reference/meya-email-component-address-ask)
    - [facebook.wit.ask.ask](https://docs.meya.ai/reference/meya-facebook-wit-component-ask-ask)
    - [google.dialogflow.ask](https://docs.meya.ai/reference/meya-google-dialogflow-component-ask)
    - [text.ask_regex](https://docs.meya.ai/reference/meya-text-component-ask_regex)
    """

    is_abstract: bool = meta_field(value=True)

    catchall: bool = element_field(
        default=True, help="Whether to return max confidence of 1.0 or not."
    )
    retries: Real = element_field(
        default=float("inf"),
        level=MetaLevel.INTERMEDIATE,
        help=(
            "The number of retries to perform should the component's "
            "validation fail."
        ),
    )
    error_message: str = element_field(
        default="Invalid input, please try again.",
        level=MetaLevel.INTERMEDIATE,
    )

    @property
    def confidence(self) -> Optional[float]:
        if self.catchall:
            return Trigger.MAX_CONFIDENCE
        else:
            return None
