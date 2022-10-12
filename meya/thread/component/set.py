from dataclasses import dataclass
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.thread.meta_tag import ThreadManagementTag
from meya.trigger.element import Trigger
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class ThreadSetComponent(Component):
    """
    Set thread-scope data.
    """

    meta_level: float = meta_field(value=MetaLevel.BASIC)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[ThreadManagementTag])

    thread_id: Optional[str] = element_field(default=None)
    thread_set: Union[str, dict] = element_field(signature=True)

    async def start(self) -> List[Entry]:
        if self.thread_id:
            await self.thread.load(self.thread_id)

        if isinstance(self.thread_set, str):
            if Trigger.RESULT_KEY not in self.entry.data:
                raise self.process_error(
                    f'Could not set thread scope property "{self.thread_set}"'
                    f" because flow.result is not set"
                )
            self.thread[self.thread_set] = self.entry.data.get(
                Trigger.RESULT_KEY
            )
        elif isinstance(self.thread_set, dict):
            for key, value in self.thread_set.items():
                self.thread[key] = value
        return self.respond()
