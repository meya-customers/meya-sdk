from dataclasses import dataclass
from meya.component.element.element import Component
from meya.element.field import element_field
from meya.twilio.voice.event.reject import RejectReason


@dataclass
class TwilioVoiceRejectComponent(Component):
    """
    # Reject
    ## Rejects an incoming call to your Twilio number without billing you.

    ## Parameters:
    #### reason: Tells Twilio what message to play when rejecting a cal
    - rejected
    - busy
    """

    reason: RejectReason = element_field()
