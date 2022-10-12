from meya.element import Element
from meya.log.element import LogElement
from meya.log.element import LogRef
from typing import ClassVar
from typing import Type


class DbLogElement(LogElement):
    async def accept_sensitive(self) -> bool:
        return await self.accept()


class DbLogRef(LogRef):
    element_type: ClassVar[Type[Element]] = DbLogElement
