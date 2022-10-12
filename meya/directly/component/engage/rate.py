from dataclasses import dataclass
from meya.directly.component.api import DirectlyApiComponent
from meya.directly.integration.api import Rating
from meya.element.field import element_field
from meya.http.entry.response import HttpResponseEntry


@dataclass
class DirectlyConversationRateComponent(DirectlyApiComponent):
    conversation_id: str = element_field()
    rating: Rating = element_field()
    user_ref_id: str = element_field()

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.conversation_rate(
            conversation_id=self.conversation_id,
            rating=self.rating,
            user_ref_id=self.user_ref_id,
        )
