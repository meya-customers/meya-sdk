from dataclasses import dataclass
from meya.component.element.element import Component
from meya.element.element import element_field


@dataclass
class TwilioVoiceDialComponent(Component):
    """
    # Dial
    ## Connect the current caller to another party.

    ## Parameters:
    #### number: number to dial
    """

    number: str = element_field()
