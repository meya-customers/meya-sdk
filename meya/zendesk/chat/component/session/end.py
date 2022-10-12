from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.zendesk.chat.integration import ZendeskChatIntegrationRef


@dataclass
class ZendeskChatSessionEndComponent(BaseApiComponent):
    integration: ZendeskChatIntegrationRef = element_field()
