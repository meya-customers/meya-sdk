from dataclasses import dataclass
from meya.directly.component.api import DirectlyApiComponent
from meya.directly.integration.api import Rating
from meya.element.field import element_field
from meya.http.entry.response import HttpResponseEntry


@dataclass
class DirectlyAutomateRateComponent(DirectlyApiComponent):
    answer_uuid: str = element_field()
    rating: Rating = element_field()

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.automate_rate(
            answer_uuid=self.answer_uuid, rating=self.rating
        )
