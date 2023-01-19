from dataclasses import dataclass
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.trigger.element import Trigger
from meya.user.meta_tag import UserManagementTag
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class UserSetComponent(Component):
    """
    Set user-scope data.
    """

    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserManagementTag])

    user_id: Optional[str] = element_field(default=None)
    user_set: Union[str, dict] = element_field(signature=True)

    async def start(self) -> List[Entry]:
        if self.user_id:
            await self.user.load(self.user_id)

        if isinstance(self.user_set, str):
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    f'Could not set user scope variable "{self.user_set}"'
                    f" because flow.result is not set"
                )
            self.user[self.user_set] = self.entry.data.get(Trigger.RESULT_KEY)
        elif isinstance(self.user_set, dict):
            for key, value in self.user_set.items():
                self.user[key] = value
        return self.respond()
