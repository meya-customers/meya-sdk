from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass
class TrackEvent:
    event: str
    userId: Optional[str] = field(default=None)
    anonymousId: Optional[str] = field(default=None)
    properties: Optional[dict] = field(default=None)
    context: Optional[dict] = field(default=None)
    timestamp: Optional[str] = field(default=None)


@dataclass
class IdentifyEvent:
    userId: Optional[str] = field(default=None)
    anonymousId: Optional[str] = field(default=None)
    traits: Optional[dict] = field(default=None)
    context: Optional[dict] = field(default=None)
    timestamp: Optional[str] = field(default=None)
