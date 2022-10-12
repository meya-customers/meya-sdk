from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.util.dict import NONE_FACTORY
from meya.util.enum import SimpleEnum
from meya.zendesk.support.payload import ZendeskSupportPayload
from meya.zendesk.support.payload.ticket_comment import (
    ZendeskSupportTicketCommentCreate,
)
from meya.zendesk.support.payload.ticket_field import (
    ZendeskSupportTicketFieldPair,
)
from typing import List
from typing import Optional


class ZendeskSupportTicketStatus(SimpleEnum):
    NEW = "new"
    OPEN = "open"
    PENDING = "pending"
    HOLD = "hold"
    SOLVED = "solved"
    CLOSED = "closed"


@dataclass
class ZendeskSupportTicketBase(ZendeskSupportPayload):
    status: ZendeskSupportTicketStatus = payload_field()
    assignee_id: Optional[int] = payload_field(default=None)
    custom_fields: List[ZendeskSupportTicketFieldPair] = payload_field(
        default_factory=list, sensitive=True
    )
    external_id: Optional[str] = payload_field(default=None)
    group_id: Optional[int] = payload_field(default=None)
    priority: Optional[str] = payload_field(default=None)
    requester_id: int = payload_field(default=None)
    tags: List[str] = payload_field(default_factory=list)
    subject: Optional[str] = payload_field(sensitive=True, default=None)
    type: Optional[str] = payload_field(default=None)
    ticket_form_id: Optional[int] = payload_field(default=None)
    brand_id: Optional[int] = payload_field(default=None)


@dataclass
class ZendeskSupportTicketGet(ZendeskSupportTicketBase):
    assignee_id: Optional[int] = payload_field(default_factory=NONE_FACTORY)
    comment_count: Optional[int] = payload_field(default_factory=NONE_FACTORY)
    created_at: str = payload_field()
    description: str = payload_field(sensitive=True)
    external_id: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    group_id: Optional[int] = payload_field(default_factory=NONE_FACTORY)
    id: int = payload_field()
    priority: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    requester_id: int = payload_field(default_factory=NONE_FACTORY)
    type: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    updated_at: str = payload_field()


@dataclass
class ZendeskSupportTicketOptionalBase(ZendeskSupportTicketBase):
    comment: Optional[ZendeskSupportTicketCommentCreate] = payload_field(
        default=None
    )
    custom_fields: Optional[
        List[ZendeskSupportTicketFieldPair]
    ] = payload_field(default=None)
    status: Optional[str] = payload_field(default=None)
    tags: Optional[List[str]] = payload_field(default=None)


@dataclass
class ZendeskSupportTicketCreate(ZendeskSupportTicketOptionalBase):
    via_followup_source_id: Optional[int] = payload_field(default=None)


@dataclass
class ZendeskSupportTicketUpdate(ZendeskSupportTicketOptionalBase):
    requester_id: Optional[int] = payload_field(default=None)
