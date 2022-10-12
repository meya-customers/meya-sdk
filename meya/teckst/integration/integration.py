from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element.interactive import InteractiveIntegration
from typing import ClassVar
from typing import Type


@dataclass
class TeckstIntegration(InteractiveIntegration):
    NAME: ClassVar[str] = "teckst"
    TECKST_CRM: ClassVar[str] = "MeyaAccount"
    teckst_client_id: str = element_field(
        help="Alphanumeric client ID provided by Teckst"
    )
    teckst_api_key: str = element_field(
        help="Alphanumeric API key provided by Teckst"
    )
    teckst_phone_number: str = element_field(
        help="Integration phone number provided by Teckst"
    )
    teckst_api_url: str = element_field(
        help="Teckst API URL, e.g. `https://api.teckst.com/v1/crm/webhook`"
    )
    meya_api_key: str = element_field(help="Meya customer-defined API key")


class TeckstIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = TeckstIntegration
