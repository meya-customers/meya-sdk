from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import meta_field


@dataclass
class ThreadManagementTag(MetaTag):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
