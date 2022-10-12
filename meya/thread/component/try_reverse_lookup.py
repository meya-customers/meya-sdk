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
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ThreadTryReverseLookupComponent(Component):
    """
    Try to find the integration thread ID linked to the current thread.
    """

    @dataclass
    class Response(ComponentResponse):
        result: Optional[str] = response_field()

    extra_alias: str = meta_field(value="thread_try_reverse_lookup")
    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[ThreadManagementTag])

    thread_id: Optional[str] = element_field(default=None)
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        if self.thread_id:
            await self.thread.load(self.thread_id)

        result = await self.thread.try_reverse_lookup(
            integration_id=self.integration.ref
        )
        return self.respond(data=self.Response(result))
