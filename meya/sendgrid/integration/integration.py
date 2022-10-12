from dataclasses import dataclass
from meya.element.field import element_field
from meya.integration.element.interactive import InteractiveIntegration
from typing import ClassVar


@dataclass
class SendgridIntegration(InteractiveIntegration):
    """
    ## DNS Setup
    First set up SPF, DKIM and MX.

    ## Inbound parse
    Create an inbound parse using default payloads (not raw payloads).

    ## Authentication
    Create an API key and use it the Meya integration setting.
    """

    NAME: ClassVar[str] = "sendgrid"

    api_key: str = element_field()
    email_address: str = element_field()
