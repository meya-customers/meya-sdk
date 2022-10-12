from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.icon.spec import IconElementSpecUnion
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult
from typing import Optional


@dataclass
class KeywordTrigger(TextTrigger, IgnorecaseMixin):
    """
    Match exact text from the user.
    """

    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/04-login-logout/login-key-2.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    snippet_default: str = meta_field(
        value="""
            keyword: start
        """
    )

    keyword: str = element_field(
        signature=True,
        help="Exact keyword to match with user text",
        level=MetaLevel.VERY_BASIC,
    )
    ignorecase: Optional[bool] = element_field(
        default=None,
        help="Ignore case when matching text",
        level=MetaLevel.INTERMEDIATE,
    )

    async def match(self) -> TriggerMatchResult:
        keyword: str = self.keyword
        text = self.entry.text

        if self.ignorecase_default_true:
            keyword = keyword.lower()
            text = text.lower()

        if keyword == text:
            return self.succeed()
        else:
            return self.fail()
