from dataclasses import dataclass
from dataclasses import field
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Optional


@dataclass
class OpenaiContentChunk:
    item_id: Optional[str] = field(default=None)
    data_source_id: Optional[str] = field(default=None)
    source: Optional[str] = field(default=None)
    source_tokens: Optional[int] = field(default=None)
    content: Optional[str] = field(default=None)
    content_tokens: Optional[int] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict) -> "OpenaiContentChunk":
        return from_dict(cls, data)

    def to_dict(self) -> dict:
        return to_dict(self)
