from dataclasses import dataclass
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.integration.element import IntegrationRef
from meya.thread.meta_tag import ThreadManagementTag
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ThreadUnlinkComponent(Component):
    """
    Unlink the current Meya thread from an integration thread.
    """

    extra_alias: str = meta_field(value="thread_unlink")
    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[ThreadManagementTag])

    thread_id: Optional[str] = element_field(default=None)
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        if self.thread_id:
            await self.thread.load(self.thread_id)

        await self.thread.unlink(integration_id=self.integration.ref)

        return self.respond()
