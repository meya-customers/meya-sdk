from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.freshworks.freshchat.event import FreshchatEvent
from meya.freshworks.freshchat.payload.agent import FreshchatAgent
from meya.freshworks.freshchat.payload.group import FreshchatGroup
from typing import Optional


@dataclass
class FreshchatAssignEvent(FreshchatEvent):
    from_agent: Optional[FreshchatAgent] = entry_field(
        default=None, sensitive=True
    )
    from_group: Optional[FreshchatGroup] = entry_field(
        default=None, sensitive=True
    )
    to_agent: Optional[FreshchatAgent] = entry_field(
        default=None, sensitive=True
    )
    to_group: Optional[FreshchatGroup] = entry_field(
        default=None, sensitive=True
    )
