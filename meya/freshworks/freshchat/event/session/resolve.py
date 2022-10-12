from dataclasses import dataclass
from meya.freshworks.freshchat.event import FreshchatEvent


@dataclass
class FreshchatResolveEvent(FreshchatEvent):
    pass
