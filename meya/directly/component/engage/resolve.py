from dataclasses import dataclass
from meya.directly.component.api import DirectlyApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse


@dataclass
class DirectlyConversationResolveComponent(DirectlyApiComponent):
    mark_as_resolved_message_id: str = element_field()
    confirm: bool = element_field()

    @dataclass
    class Response(ApiComponentResponse):
        conversation_id: str = response_field()
        user_ref_id: str = response_field()

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.conversation_resolve(
            message_id=self.mark_as_resolved_message_id,
            confirm=self.confirm,
            user_ref_id=await self.get_user_ref_id(),
        )

    async def on_response(self, response: ApiComponentResponse):
        response.conversation_id = await self.get_conversation_id()
        response.user_ref_id = await self.get_user_ref_id()
