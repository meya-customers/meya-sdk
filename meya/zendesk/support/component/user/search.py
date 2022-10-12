from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.sort import ZendeskSupportSortOrder
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportUserSearchComponent(BaseApiComponent):
    @dataclass
    class Response:
        result: List[ZendeskSupportUserGet] = response_field(sensitive=True)
        count: int = response_field()

    integration: ZendeskSupportIntegrationRef = element_field()
    query: List[str] = element_field()
    sort_by: Optional[str] = element_field(default=None)
    sort_order: Optional[ZendeskSupportSortOrder] = element_field(default=None)
