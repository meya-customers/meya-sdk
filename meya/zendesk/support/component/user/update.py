from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportUserUpdateComponent(BaseApiComponent):
    @dataclass
    class Response:
        result: ZendeskSupportUserGet = response_field(sensitive=True)

    integration: ZendeskSupportIntegrationRef = element_field()
    user_id: Optional[int] = element_field(default=None)
    name: Optional[str] = element_field(default=None)
    details: Optional[str] = element_field(default=None)
    email: Optional[str] = element_field(default=None)
    verified: Optional[bool] = element_field(default=None)
    phone: Optional[str] = element_field(default=None)
    tags: Optional[List[str]] = element_field(default=None)
    user_fields: Optional[Dict[str, Any]] = element_field(default=None)
    external_id: Optional[str] = element_field(default=None)
