from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.zendesk.help_center.payload import ZendeskHelpCenterBaseResponse
from typing import List
from typing import Optional


@dataclass
class ZendeskHelpCenterCategory(Payload):
    created_at: Optional[str] = payload_field(default=None)
    description: Optional[str] = payload_field(default=None)
    html_url: Optional[str] = payload_field(default=None)
    id: Optional[int] = payload_field(default=None)
    locale: Optional[str] = payload_field(default=None)
    name: str = payload_field()
    outdated: Optional[str] = payload_field(default=None)
    position: int = payload_field()
    source_locale: Optional[str] = payload_field(default=None)
    updated_at: Optional[str] = payload_field(default=None)
    url: Optional[str] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterCategoryRequest(Payload):
    category: ZendeskHelpCenterCategory = payload_field()


@dataclass
class ZendeskHelpCenterCategoryResponse(Payload):
    category: ZendeskHelpCenterCategory = payload_field()


@dataclass
class ZendeskHelpCenterCategoriesResponse(ZendeskHelpCenterBaseResponse):
    categories: List[ZendeskHelpCenterCategory] = payload_field(
        default_factory=list
    )
