from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.util.dict import NONE_FACTORY
from meya.util.enum import SimpleEnum
from meya.zendesk.support.payload import ZendeskSupportPayload
from meya.zendesk.support.payload.attachment import ZendeskSupportAttachment
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class ZendeskSupportUserRole(SimpleEnum):
    END_USER = "end-user"
    AGENT = "agent"
    ADMIN = "admin"
    SYSTEM = "system"


@dataclass
class ZendeskSupportUserBase(ZendeskSupportPayload):
    alias: Optional[str] = payload_field(default=None)
    details: Optional[str] = payload_field(default=None)
    email: Optional[str] = payload_field(default=None)
    external_id: Optional[str] = payload_field(default=None)
    name: str = payload_field()
    phone: Optional[str] = payload_field(default=None)
    tags: List[str] = payload_field(default_factory=list)
    user_fields: Dict[str, Any] = payload_field(default_factory=dict)
    verified: bool = payload_field()


@dataclass
class ZendeskSupportUserGet(ZendeskSupportUserBase):
    alias: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    created_at: str = payload_field()
    details: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    email: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    external_id: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    id: int = payload_field()
    phone: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    photo: Optional[ZendeskSupportAttachment] = payload_field(
        default_factory=NONE_FACTORY
    )
    role: ZendeskSupportUserRole = payload_field()
    updated_at: str = payload_field()


@dataclass
class ZendeskSupportUserOptionalBase(ZendeskSupportUserBase):
    tags: Optional[List[str]] = payload_field(default=None)
    user_fields: Optional[Dict[str, Any]] = payload_field(default=None)
    verified: Optional[bool] = payload_field(default=None)


@dataclass
class ZendeskSupportUserCreate(ZendeskSupportUserOptionalBase):
    pass


@dataclass
class ZendeskSupportUserUpdate(ZendeskSupportUserOptionalBase):
    name: Optional[str] = payload_field(default=None)
