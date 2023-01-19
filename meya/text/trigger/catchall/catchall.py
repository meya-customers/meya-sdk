from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import meta_field
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult


@dataclass
class CatchallTrigger(TextTrigger):
    """
    Match any text from the user.

    https://docs.meya.ai/docs/triggers-1#catchall-trigger
    """

    extra_alias: str = meta_field(value="catchall")
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)

    async def match(self) -> TriggerMatchResult:
        return self.succeed(confidence=self.MIN_CONFIDENCE)
