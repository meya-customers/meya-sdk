from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.twilio.integration.base import TwilioBaseIntegration
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from meya.voice.integration.integration import VoiceIntegration
from typing import ClassVar
from typing import Type


@dataclass
class TwilioVoiceIntegration(VoiceIntegration, TwilioBaseIntegration):
    """
    ## Setup
    - Add Twilio Voice integration to your app
    - Get integration webhook (run `meya webhooks`)
    - Open your Twilio Voice [phone number settings](https://www.twilio.com/console/phone-numbers/incoming)
    - Set integration webhook to Twilio Voice "A CALL COMES IN" option
    """

    NAME: ClassVar[str] = "twilio_voice"
    phone_number: str = element_field(
        help="Twilio active number for use with Meya"
    )


class TwilioVoiceIntegrationRef(TwilioBaseIntegrationRef):
    element_type: ClassVar[Type[Element]] = TwilioVoiceIntegration
