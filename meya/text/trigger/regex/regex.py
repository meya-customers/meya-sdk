import re

from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult
from typing import Any
from typing import Optional
from typing import Tuple


@dataclass
class RegexTriggerResponse:
    result: str = response_field(sensitive=True, default="")
    groups: dict = response_field(sensitive=True)


@dataclass
class RegexTrigger(TextTrigger, IgnorecaseMixin):
    GROUPS_KEY = "groups"

    meta_level: float = meta_field(value=MetaLevel.BASIC)

    regex: str = element_field(signature=True)
    ignorecase: Optional[bool] = element_field(default=None)

    async def match(self) -> TriggerMatchResult:
        match = self.search_regex(
            self.regex, self.entry.text, self.ignorecase_default_true
        )
        if match:
            match_result, match_groups = match
        else:
            match_result = ""
            match_groups = {}

        if self.confidence is not None or match:
            confidence = self.confidence or self.MAX_CONFIDENCE
            return self.succeed(
                confidence=confidence,
                data=RegexTriggerResponse(
                    result=match_result, groups=match_groups
                ),
            )
        else:
            return self.fail()

    @staticmethod
    def search_regex(
        regex: str, string: Any, ignorecase: bool
    ) -> Optional[Tuple[str, dict]]:
        if not isinstance(string, str):
            return None

        if ignorecase:
            flags = re.IGNORECASE
        else:
            flags = 0

        match = re.search(regex, string, flags=re.VERBOSE | flags)
        if match:
            return (
                match.group(0),
                {**dict(enumerate([*match.groups()])), **match.groupdict()},
            )
        else:
            return None
