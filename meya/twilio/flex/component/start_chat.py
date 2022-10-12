from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.twilio.flex.payload.channel import CreateFlexChannelResponse
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from typing import Optional


@dataclass
class TwilioFlexStartChatComponent(BaseApiComponent):
    """
    Learn more: https://www.twilio.com/docs/flex/developer/messaging/api/chat-channel
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: CreateFlexChannelResponse = response_field()

    send_transcript: bool = element_field(
        default=True,
        help="Send the conversation transcript to flex agent when chat is accepted",
    )
    chat_friendly_name: str = element_field(
        help='Chat title. This is the only information the flex agent will see before chat is accepted, should be very informative e.g. "James - +55112222222222 - computer problem"'
    )
    task_attributes: Optional[dict] = element_field(
        default=None,
        help="Used for routing purposes. Check twilio docs https://www.twilio.com/taskrouter",
    )
    integration: TwilioBaseIntegrationRef = element_field()
