from meya.util.enum import SimpleEnum
from typing import List
from typing import Union


class MarkdownFeature(SimpleEnum):
    FORMAT = "format"
    LINKIFY = "linkify"
    BREAKS = "breaks"
    TYPOGRAPHER = "typographer"


MarkdownEventSpec = List[MarkdownFeature]
MarkdownElementSpec = List[MarkdownFeature]

MarkdownElementSpecUnion = Union[MarkdownElementSpec, bool]


class MarkdownEventSpecHelper:
    @staticmethod
    def from_element_spec(
        markdown: MarkdownElementSpecUnion,
    ) -> MarkdownEventSpec:
        if markdown is False:
            return []
        elif markdown is True:
            return [
                MarkdownFeature.FORMAT,
                MarkdownFeature.LINKIFY,
                MarkdownFeature.BREAKS,
                MarkdownFeature.TYPOGRAPHER,
            ]
        else:
            return markdown
