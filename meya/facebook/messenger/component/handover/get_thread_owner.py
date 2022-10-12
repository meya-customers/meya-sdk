from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.facebook.messenger.element.mixin import FacebookMessengerMixin
from meya.integration.element.api import ApiComponentResponse
from typing import Any
from typing import Dict


@dataclass
class FacebookMessengerGetThreadOwnerComponent(
    BaseApiComponent, FacebookMessengerMixin
):
    @dataclass
    class Response(ApiComponentResponse):
        result: Dict[str, Any] = response_field(sensitive=True)

    recipient_id: str = element_field(help="Facebook Messenger recipient ID")
