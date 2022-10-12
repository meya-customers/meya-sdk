from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.teckst.integration import TeckstIntegrationRef


@dataclass
class TeckstMixin(Element):
    phone_number: str = element_field(
        help="Phone number to receive the message"
    )
    integration: TeckstIntegrationRef = element_field(
        help="Send with this Teckst integration"
    )
