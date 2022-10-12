from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element import Integration
from typing import ClassVar
from typing import Type


@dataclass
class SlackIntegration(Integration):
    NAME: ClassVar[str] = "slack"

    webhook_url: str = element_field()

    async def accept(self) -> bool:
        return False


class SlackIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = SlackIntegration
