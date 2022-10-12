from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.zendesk.base.integration import ZendeskBaseIntegration
from typing import ClassVar
from typing import Type


@dataclass
class ZendeskHelpCenterIntegration(ZendeskBaseIntegration):
    NAME: ClassVar[str] = "zendesk_help_center"

    async def accept(self) -> bool:
        return False


class ZendeskHelpCenterIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = ZendeskHelpCenterIntegration
