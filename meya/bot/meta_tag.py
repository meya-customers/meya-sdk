from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpecUnion


@dataclass
class BotOutputTag(MetaTag):
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/21-messages-chat-smileys/02-messages-speech-bubbles/messages-bubble-text-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.BASIC)


@dataclass
class BotFlowTag(MetaTag):
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/52-arrows-diagrams/02-diagrams/diagram-curve-up-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.BASIC)
