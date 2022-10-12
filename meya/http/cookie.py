from dataclasses import dataclass
from typing import Optional


@dataclass
class Cookie:
    http_only: Optional[bool]
    max_age: Optional[int]
    secure: Optional[bool]
    value: str
