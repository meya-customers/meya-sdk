from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpecUnion


@dataclass
class TimeTag(MetaTag):
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/18-time/hourglass-1.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
