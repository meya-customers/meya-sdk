from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from typing import Optional


@dataclass
class TwilioFlexEndChatComponent(BaseApiComponent):
    """
    Learn more: https://www.twilio.com/docs/flex/developer/messaging/api/chat-channel
    """

    text: Optional[str] = element_field(
        default=None,
        help="The last message sent to the agent before closing the Flex channel.",
    )
    integration: TwilioBaseIntegrationRef = element_field()
