from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.facebook.messenger.integration.integration import (
    FacebookMessengerIntegrationRef,
)


@dataclass
class FacebookMessengerMixin(Element):
    page_id: int = element_field(default="Facebook Messenger Page ID")
    integration: FacebookMessengerIntegrationRef = element_field(
        help="Facebook Messenger integration reference"
    )
