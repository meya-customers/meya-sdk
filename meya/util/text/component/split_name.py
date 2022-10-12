from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from typing import List


def split_name(name: str) -> (str, str):
    if name is None:
        return None, None
    parts = name.split(" ")
    if len(parts) > 1:
        return parts[0], " ".join(parts[1:])
    else:
        return name, ""


@dataclass
class SplitNameResponse:
    first_name: str = response_field(sensitive=True)
    last_name: str = response_field(sensitive=True)


@dataclass
class SplitNameComponent(Component):
    name: str = element_field()

    async def start(self) -> List[Entry]:
        response = SplitNameResponse(*split_name(self.name))
        return self.respond(data=dict(result=response))
