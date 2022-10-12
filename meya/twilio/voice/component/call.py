from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.element import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.twilio.voice.integration.integration import TwilioVoiceIntegrationRef
from meya.twilio.voice.payload.call import TwilioVoiceCallPayload


@dataclass
class TwilioVoiceCallComponent(BaseApiComponent):
    """
    # Call
    ## Create outbound call

    ## Parameters:
    #### to: number to call (end user)
    """

    @dataclass
    class Response(ApiComponentResponse):
        result: TwilioVoiceCallPayload = response_field(sensitive=True)

    to: str = element_field()
    integration: TwilioVoiceIntegrationRef = element_field()
