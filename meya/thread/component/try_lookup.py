from dataclasses import dataclass
from meya.component.element import Component
from meya.component.element import ComponentResponse
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.db.view.thread import ThreadView
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
class ThreadTryLookupComponent(Component):
    """
    Try to find the thread ID linked to an integration thread.
    """

    @dataclass
    class Response(ComponentResponse):
        result: Optional[str] = response_field()

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[ThreadManagementTag])

    thread_try_lookup: str = element_field(
        signature=True, help="The integration ID to look up"
    )
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        result = await ThreadView.try_lookup(
            self.thread_try_lookup, integration_id=self.integration.ref
        )
        return self.respond(data=self.Response(result))
