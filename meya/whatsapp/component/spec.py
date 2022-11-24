from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonElementSpec
from meya.core.meta_level import MetaLevel
from typing import Optional


@dataclass
class ListPickerItemElementSpec(ButtonElementSpec):
    text: Optional[str] = field(
        default=None,
        metadata=dict(help="The list item's text", level=MetaLevel.VERY_BASIC),
    )
    description: Optional[str] = field(
        default=None,
        metadata=dict(
            help="The list item's description", level=MetaLevel.VERY_BASIC
        ),
    )

    @staticmethod
    def get_snippet_default() -> str:
        return """
            text: Select me
            description: Select to continue
            action: next
        """
