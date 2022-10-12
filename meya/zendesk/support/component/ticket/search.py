from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.sort import ZendeskSupportSortOrder
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportTicketSearchComponent(BaseApiComponent, ZendeskBaseMixin):
    @dataclass
    class Response:
        result: List[ZendeskSupportTicketGet] = response_field(sensitive=True)
        count: int = response_field()

    query: List[str] = element_field()
    sort_by: Optional[str] = element_field(default=None)
    sort_order: Optional[ZendeskSupportSortOrder] = element_field(default=None)
