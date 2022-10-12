from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.sunshine_conversations.integration import (
    SunshineConversationsIntegrationRef,
)
from meya.zendesk.sunshine_conversations.payload.user import SunshineAppUser
from typing import Optional


@dataclass
class SunshineConversationsAppUserGetComponent(BaseApiComponent):
    @dataclass
    class Response:
        result: SunshineAppUser = response_field(sensitive=True)

    integration: SunshineConversationsIntegrationRef = element_field()
    user_id: Optional[str] = element_field(default=None)
    external_id: Optional[str] = element_field(default=None)
