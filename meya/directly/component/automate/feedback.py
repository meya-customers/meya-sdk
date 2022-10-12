from dataclasses import dataclass
from meya.directly.component.api import DirectlyApiComponent
from meya.directly.integration.api import QuickReply
from meya.element.field import element_field
from meya.http.entry.response import HttpResponseEntry


@dataclass
class DirectlyAutomateFeedbackComponent(DirectlyApiComponent):
    answer_uuid: str = element_field()
    quick_reply: QuickReply = element_field()

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.automate_feedback(
            answer_uuid=self.answer_uuid, quick_reply=self.quick_reply
        )
