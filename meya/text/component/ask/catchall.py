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
    is_abstract: bool = meta_field(value=True)

    catchall: bool = element_field(default=True)
    retries: Real = element_field(
        default=float("inf"), level=MetaLevel.INTERMEDIATE
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
