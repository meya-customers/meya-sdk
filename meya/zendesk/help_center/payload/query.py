from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from meya.zendesk.help_center.payload import ZendeskHelpCenterBaseResponse
from meya.zendesk.help_center.payload.article import ZendeskHelpCenterArticle
from typing import List
from typing import Optional
from typing import Union


class ZendeskHelpCenterSortBy(SimpleEnum):
    POSITION = "position"
    TITLE = "title"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class ZendeskHelpCenterSortOrder(SimpleEnum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class ZendeskHelpCenterPagination(Payload):
    page: Optional[int] = payload_field(default=None)
    per_page: Optional[int] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterSort(ZendeskHelpCenterPagination):
    sort_by: Optional[ZendeskHelpCenterSortBy] = payload_field(default=None)
    sort_order: Optional[ZendeskHelpCenterSortOrder] = payload_field(
        default=None
    )


@dataclass
class ZendeskHelpCenterSearchRequest(ZendeskHelpCenterSort):
    query: str = payload_field()
    brand_id: Optional[int] = payload_field(default=None)
    category: Optional[Union[int, str]] = payload_field(default=None)
    created_after: Optional[str] = payload_field(default=None)
    created_at: Optional[str] = payload_field(default=None)
    created_before: Optional[str] = payload_field(default=None)
    label_names: Optional[str] = payload_field(default=None)
    locale: Optional[str] = payload_field(default=None)
    multibrand: Optional[bool] = payload_field(default=None)
    section: Optional[Union[int, str]] = payload_field(default=None)
    updated_after: Optional[str] = payload_field(default=None)
    updated_at: Optional[str] = payload_field(default=None)
    updated_before: Optional[str] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterArticleSearchResponse(ZendeskHelpCenterArticle):
    result_type: str = payload_field()
    snippet: str = payload_field()


@dataclass
class ZendeskHelpCenterSearchResponse(ZendeskHelpCenterBaseResponse):
    results: List[ZendeskHelpCenterArticleSearchResponse] = payload_field()
