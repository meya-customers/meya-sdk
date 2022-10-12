from dataclasses import dataclass
from http import HTTPStatus
from meya.component.element import Component
from meya.element.field import response_field
from meya.entry import Entry
from typing import List
from typing import Optional


@dataclass
class JokeComponentResponse:
    ok: bool = response_field()
    setup: Optional[str] = response_field()
    punchline: Optional[str] = response_field()


@dataclass
class JokeComponent(Component):
    async def start(self) -> List[Entry]:
        res = await self.http.get(
            "https://official-joke-api.appspot.com/random_joke"
        )
        if res.status != HTTPStatus.OK:
            return self.respond(data=JokeComponentResponse(ok=False))
        else:
            return self.respond(
                data=JokeComponentResponse(
                    ok=True,
                    setup=res.data["setup"],
                    punchline=res.data["punchline"],
                )
            )
