from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from meya.util.form_data import BinaryFile
from numbers import Real
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


"""
https://dev.frontapp.com/reference/contacts
"""


class FrontSource(SimpleEnum):
    EMAIL = "email"
    PHONE = "phone"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INTERCOM = "intercom"
    FRONT_CHAT = "front_chat"
    CUSTOM = "custom"


@dataclass
class FrontContactHandleBase(FrontPayload):
    handle: str = payload_field()
    source: FrontSource = payload_field()


@dataclass
class FrontContactCreateHandle(FrontContactHandleBase):
    pass


@dataclass
class FrontAddContactHandle(FrontContactHandleBase):
    pass


@dataclass
class FrontDeleteContactHandle(FrontContactHandleBase):
    force: bool = payload_field(default=False)


@dataclass
class FrontContact(FrontPayload):
    name: Optional[str] = payload_field(default=None)
    description: Optional[str] = payload_field(default=None)
    avatar: Optional[BinaryFile] = payload_field(default=None)
    is_spammer: Optional[bool] = payload_field(default=None)
    group_names: Optional[List[str]] = payload_field(default=None)
    links: Optional[List[str]] = payload_field(default=None)
    custom_fields: Optional[Dict[str, Any]] = payload_field(default=None)
    handles: Optional[List[FrontContactCreateHandle]] = payload_field(
        default=None
    )


@dataclass
class FrontContactCreateRelated:
    notes: Optional[str] = payload_field(default=None)
    conversations: Optional[str] = payload_field(default=None)


@dataclass
class FrontContactCreateLinks:
    related: FrontContactCreateRelated = payload_field(
        default_factory=FrontContactCreateRelated
    )


@dataclass
class FrontContactCreateResponse(FrontPayload):
    id: str = payload_field()
    description: str = payload_field()
    links: FrontContactCreateLinks = payload_field(key="_links")
    updated_at: Real = payload_field()
    is_private: bool = payload_field()
    name: Optional[str] = payload_field(default=None)
    avatar_url: Optional[str] = payload_field(default=None)
    groups: List[str] = payload_field(default_factory=list)
    handles: Optional[List[FrontContactCreateHandle]] = payload_field(
        default_factory=list
    )
    custom_fields: Dict[str, Any] = payload_field(default_factory=dict)

    @property
    def handle(self) -> str:
        if self.handles:
            for handle_obj in self.handles:
                if handle_obj.source == FrontSource.CUSTOM:
                    return handle_obj.handle


@dataclass
class FrontContactUpdateResponse(FrontPayload):
    id: str = payload_field()


@dataclass
class FrontContactGet(FrontContactCreateResponse):
    pass


@dataclass
class FrontContactCreateOrUpdate(FrontContactUpdateResponse):
    id: str = payload_field()
    handle: str = payload_field()
