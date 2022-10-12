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
from meya.user.meta_tag import UserManagementTag
from typing import List
from typing import Optional
from typing import Type


@dataclass
class UserTryReverseLookupComponent(Component):
    """
    Try to find the integration user ID linked to the current user.
    """

    @dataclass
    class Response(ComponentResponse):
        result: Optional[str] = response_field()

    extra_alias: str = meta_field(value="user_try_reverse_lookup")
    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_id: Optional[str] = element_field(default=None)
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        if self.user_id:
            await self.user.load(self.user_id)

        result = await self.user.try_reverse_lookup(
            integration_id=self.integration.ref
        )
        return self.respond(data=self.Response(result))
