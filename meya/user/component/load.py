from dataclasses import dataclass
from meya.component.element import Component
from meya.component.element import ComponentResponse
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.user.meta_tag import UserManagementTag
from typing import Any
from typing import Dict
from typing import List
from typing import Type


@dataclass
class UserLoadComponent(Component):
    """
    Load data for a specific user.
    """

    @dataclass
    class Response(ComponentResponse):
        result: Dict[str, Any] = response_field()

    meta_level: float = meta_field(value=MetaLevel.VERY_ADVANCED)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_load: str = element_field(signature=True, help="The user ID to load")

    async def start(self) -> List[Entry]:
        await self.user.load(self.user_load)
        return self.respond(data=self.Response(self.user.data))
