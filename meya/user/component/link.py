from dataclasses import dataclass
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.integration.element import IntegrationRef
from meya.user.meta_tag import UserManagementTag
from typing import List
from typing import Optional
from typing import Type


@dataclass
class UserLinkComponent(Component):
    """
    Link the current Meya user to an integration user, allowing only this
    single link.
    """

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_id: Optional[str] = element_field(default=None)
    user_link: str = element_field(
        signature=True, help="The integration user ID to link"
    )
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        if self.user_id:
            await self.user.load(self.user_id)

        await self.user.link(
            self.user_link, integration_id=self.integration.ref
        )

        return self.respond()
