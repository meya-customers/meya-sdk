from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element import Integration
from typing import ClassVar
from typing import Type


@dataclass
class WitIntegration(Integration):
    NAME: ClassVar[str] = "wit"

    api_token: str = element_field(help="Your Wit server access token.")

    async def accept(self) -> bool:
        return False


class WitIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = WitIntegration
