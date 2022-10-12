from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.front.payload.payload import FrontBaseResponse
from meya.front.payload.teammate import FrontTeammateGet
from meya.http.payload.field import payload_field
from meya.util.dict import MISSING_FACTORY
from typing import List
from typing import Optional


"""
https://dev.frontapp.com/reference/conversations-1
"""


@dataclass
class FrontConversationBase(FrontPayload):
    status: str = payload_field()


@dataclass
class FrontConversationGet(FrontConversationBase):
    id: str = payload_field()
    subject: str = payload_field()
    assignee: Optional[FrontTeammateGet] = payload_field(default=None)


@dataclass
class FrontConversationUpdate(FrontConversationBase):
    assignee_id: Optional[str] = payload_field(default_factory=MISSING_FACTORY)
    inbox_id: Optional[str] = payload_field(default=None)
    status: Optional[str] = payload_field(default=None)
    tag_ids: Optional[List[str]] = payload_field(default=None)


@dataclass
class FrontCreateConversationResponse(FrontBaseResponse):
    conversation_id: Optional[str] = payload_field(default=None)
