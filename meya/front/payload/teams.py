from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.front.payload.payload import FrontPagination
from meya.front.payload.teammate import FrontTeammateGet
from meya.http.payload.field import payload_field
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class FrontInboxLinks(FrontPayload):
    channels: Optional[str] = payload_field(default=None)
    conversations: Optional[str] = payload_field(default=None)
    teammates: Optional[str] = payload_field(default=None)
    owner: Optional[str] = payload_field(default=None)


@dataclass
class FrontInboxLinksRelated(FrontPayload):
    related: FrontInboxLinks = payload_field()


@dataclass
class FrontInbox(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()
    is_private: Optional[bool] = payload_field(default=None)
    is_public: Optional[bool] = payload_field(default=None)
    custom_fields: Optional[Dict[str, Any]] = payload_field(
        default_factory=dict
    )
    links: Optional[FrontInboxLinksRelated] = payload_field(
        default=None, key="_links"
    )


@dataclass
class FrontTeam(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()
    inboxes: List[FrontInbox] = payload_field(default_factory=list)
    members: List[FrontTeammateGet] = payload_field(default_factory=list)


@dataclass
class FrontTeamsData(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()


@dataclass
class FrontTeams(FrontPayload):
    pagination: FrontPagination = payload_field(key="_pagination")
    results: Optional[List[FrontTeamsData]] = payload_field(
        key="_results", default_factory=list
    )
