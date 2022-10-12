from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.zendesk.chat.integration import ZendeskChatIntegrationRef
from typing import List
from typing import Optional


@dataclass
class ZendeskChatSessionStartComponent(BaseApiComponent):
    integration: ZendeskChatIntegrationRef = element_field()
    visitor_name: Optional[str] = element_field(default=None)
    visitor_email: Optional[str] = element_field(default=None)
    visitor_phone: Optional[str] = element_field(default=None)
    visitor_url: Optional[str] = element_field(default=None)
    visitor_user_agent: Optional[str] = element_field(default=None)
    visitor_referrer: Optional[str] = element_field(default=None)
    tags: Optional[List[str]] = element_field(default=None)
    department: Optional[str] = element_field(default=None)
