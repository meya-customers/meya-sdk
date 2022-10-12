import meya.util.uuid

from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import response_field
from meya.entry import Entry
from typing import List


@dataclass
class RandomHexComponent(Component):
    @dataclass
    class Response:
        result: str = response_field(sensitive=True)

    async def start(self) -> List[Entry]:
        return self.respond(
            data=self.Response(result=meya.util.uuid.uuid4_hex())
        )
