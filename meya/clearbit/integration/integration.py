from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element import Integration
from typing import ClassVar
from typing import Type


@dataclass
class ClearbitIntegration(Integration):
    NAME: ClassVar[str] = "clearbit"

    api_key: str = element_field()

    async def accept(self) -> bool:
        return False


class ClearbitIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = ClearbitIntegration
