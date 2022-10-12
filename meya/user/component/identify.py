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
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type


@dataclass
class UserIdentifyComponent(Component):
    """
    Find and load the Meya user linked to from an integration user.

    - If not linked yet, create a new Meya user
    - If data provided, merge into loaded user data
    - If default data provided, merge into loaded user data for keys not yet
      set
    """

    @dataclass
    class Response(ComponentResponse):
        result: str = response_field()

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_identify: str = element_field(
        signature=True, help="The integration user ID to identify"
    )
    integration: IntegrationRef = element_field()
    data: Optional[Dict[str, Any]] = element_field(default=None)
    default_data: Optional[Dict[str, Any]] = element_field(default=None)

    async def start(self) -> List[Entry]:
        await self.user.identify(
            self.user_identify,
            integration_id=self.integration.ref,
            data=self.data,
            default_data=self.default_data,
        )
        return self.respond(data=self.Response(self.user.id))
