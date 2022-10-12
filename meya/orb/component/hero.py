from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.entry import Entry
from meya.orb.event.hero import HeroEvent
from typing import List
from typing import Optional


@dataclass
class HeroComponent(InteractiveComponent):
    hero: Optional[str] = element_field(signature=True)
    description: Optional[str] = element_field(default=None)

    async def start(self) -> List[Entry]:
        hero_event = HeroEvent(description=self.description, title=self.hero)
        return self.respond(hero_event)
