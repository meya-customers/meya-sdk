from dataclasses import dataclass
from typing import Optional


@dataclass
class FreshchatGroup:
    id: str
    name: str
    description: Optional[str]
    routing_type: str
