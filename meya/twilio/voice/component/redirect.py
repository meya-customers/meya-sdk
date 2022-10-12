from dataclasses import dataclass
from meya.component.element.element import Component
from meya.element.field import element_field
from typing import Optional


@dataclass
class TwilioVoiceRedirectComponent(Component):
    """
    # Redirect
    ## Transfers control of a call to the TwiML at a different URL

    ## Parameters:
    #### url
    #### method: GET/POST
    """

    url: str = element_field()
    method: str = element_field()
