from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import Optional


@dataclass
class ZendeskSupportUserShowComponent(BaseApiComponent):
    @dataclass
    class Response:
        result: ZendeskSupportUserGet = response_field(sensitive=True)

    integration: ZendeskSupportIntegrationRef = element_field()
    user_id: Optional[int] = element_field(default=None)
    bot_agent: bool = element_field(default=False)
