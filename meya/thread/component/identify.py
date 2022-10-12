from dataclasses import dataclass
from meya.component.element import Component
from meya.component.element import ComponentResponse
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.integration.element import IntegrationRef
from meya.thread.meta_tag import ThreadManagementTag
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ThreadIdentifyComponent(Component):
    """
    Find and load the Meya thread linked to from an integration thread.

    - If not linked yet, create a new Meya thread
    - If data provided, merge into loaded thread data
    - If default data provided, merge into loaded thread data for keys not yet
      set
    """

    @dataclass
    class Response(ComponentResponse):
        result: str = response_field()

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[ThreadManagementTag])

    thread_identify: str = element_field(
        signature=True, help="The integration thread ID to identify"
    )
    integration: IntegrationRef = element_field()
    data: Optional[Dict[str, Any]] = element_field(default=None)
    default_data: Optional[Dict[str, Any]] = element_field(default=None)

    async def start(self) -> List[Entry]:
        await self.thread.identify(
            self.thread_identify,
            integration_id=self.integration.ref,
            data=self.data,
            default_data=self.default_data,
        )
        return self.respond(data=self.Response(self.thread.id))
