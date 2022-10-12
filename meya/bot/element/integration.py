from dataclasses import dataclass
from meya.element.field import meta_field
from meya.integration.element import Integration
from typing import ClassVar


@dataclass
class BotIntegration(Integration):
    NAME: ClassVar[str] = "meya"

    is_abstract: bool = meta_field(value=True)

    async def accept(self) -> bool:
        return False


default_bot_integration = BotIntegration(id="meya")
