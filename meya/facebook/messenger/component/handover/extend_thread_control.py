from dataclasses import dataclass
from datetime import timedelta
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.facebook.messenger.element.mixin import FacebookMessengerMixin
from meya.integration.element.api import ApiComponentResponse
from typing import Any
from typing import Dict


@dataclass
class FacebookMessengerExtendThreadControlComponent(
    BaseApiComponent, FacebookMessengerMixin
):
    @dataclass
    class Response(ApiComponentResponse):
        result: Dict[str, Any] = response_field(sensitive=True)

    recipient_id: str = element_field(help="Facebook Messenger recipient ID")
    duration: timedelta = element_field(
        help="Duration to extend the thread control in seconds"
    )
