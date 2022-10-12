from dataclasses import dataclass
from http import HTTPStatus
from meya.directly.component.api import DirectlyApiComponent
from meya.directly.integration import DirectlyIntegration
from meya.directly.integration import DirectlyThreadMode
from meya.element.field import element_field
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Set

DEFAULT_TEXT = "-"


@dataclass
class DirectlyConversationComponent(DirectlyApiComponent):
    text: Optional[str] = element_field(default=None)
    name: Optional[str] = element_field(default=None)

    ok_status: ClassVar[Set[int]] = {HTTPStatus.CREATED}

    async def make_request(self) -> HttpResponseEntry:
        kwargs = dict(
            text=await self.get_text(self.integration_obj), user_name=self.name
        )
        # reuse same user if a question is already asked
        user_ref_id = await self.user.try_reverse_lookup(
            integration_id=self.integration_obj.id
        )
        if user_ref_id:
            kwargs["user_ref_id"] = user_ref_id
        return await self.api.new_conversation(**kwargs)

    async def on_response(self, response: ApiComponentResponse) -> Any:
        if response.ok:
            # values to reference a conversation
            conversation_id = response.result["conversationId"]
            message = response.result["messages"][0]
            actor = message["actor"]
            user_ref_id = actor["refId"]
            await self.thread.link(
                conversation_id, integration_id=self.integration_obj.id
            )
            await self.user.link(
                user_ref_id, integration_id=self.integration_obj.id
            )
            self.thread.mode = DirectlyThreadMode.EXPERT_PENDING

    async def get_text(self, integration: DirectlyIntegration) -> str:
        # use provided text
        if self.text:
            return self.text

        # default to transcript history
        return (
            "\n".join(await integration.get_transcript_lines()) or DEFAULT_TEXT
        )
