from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Optional


@dataclass
class FreshchatAvatar:
    url: Optional[str]


@dataclass
class FreshchatSocialProfile:
    type: str
    id: str


@dataclass
class FreshchatAgent:
    biography: Optional[str]
    groups: Optional[List[Any]]
    status: Optional[int]
    id: str
    first_name: str
    last_name: str
    email: str
    avatar: FreshchatAvatar
    social_profiles: List[FreshchatSocialProfile]
