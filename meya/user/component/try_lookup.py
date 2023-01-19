from dataclasses import dataclass
from meya.component.element import Component
from meya.component.element import ComponentResponse
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.db.view.user import UserView
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
class UserTryLookupComponent(Component):
    """
    Try to find the user ID linked to an integration user.
    """

    @dataclass
    class Response(ComponentResponse):
        result: Optional[str] = response_field()

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_try_lookup: str = element_field(
        signature=True, help="The integration user ID to look up."
    )
    integration: IntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        result = await UserView.try_lookup(
            self.user_try_lookup, integration_id=self.integration.ref
        )
        return self.respond(data=self.Response(result))
