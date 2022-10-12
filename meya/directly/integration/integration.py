from dataclasses import dataclass
from http import HTTPStatus
from meya.csp.event.agent.command import AgentCommandEvent
from meya.csp.integration import CspIntegration
from meya.db.view.thread import ThreadMode
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserType
from meya.directly.integration.api import ApiVersion
from meya.directly.integration.api import DirectlyApi
from meya.directly.payload.payload import DirectlyWebhookPayload
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.entry import Entry
from meya.http.payload import PayloadError
from meya.text.event.say import SayEvent
from meya.util.dict import to_dict
from numbers import Real
from typing import ClassVar
from typing import List
from typing import Type


class DirectlyThreadMode(ThreadMode):
    pass


DirectlyThreadMode.EXPERT_PENDING = DirectlyThreadMode("expert_pending")
DirectlyThreadMode.EXPERT = DirectlyThreadMode("expert")


@dataclass
class DirectlyIntegration(CspIntegration):
    NAME: ClassVar[str] = "directly"

    domain: str = element_field()
    client_id: str = element_field()
    client_secret: str = element_field()
    api_timeout: Real = element_field(default=6)

    async def rx(self) -> List[Entry]:
        try:
            payload = DirectlyWebhookPayload.from_dict(self.entry.data)
        except PayloadError as e:
            # quick return 200 if their is a problem deserializing payload
            self.log.exception()
            return self.respond(
                status=HTTPStatus.OK,
                data=self.RxResponse(
                    ok=False, accepted=False, error=f"payload_error: {e}"
                ),
            )

        # (1) lookup and load thread
        thread_id = await ThreadView.try_lookup(payload.question_uuid)
        if not thread_id:
            return self.respond(
                status=HTTPStatus.OK,
                data=self.RxResponse(ok=True, accepted=False),
            )
        await self.thread.load(thread_id)

        # (2) identify user
        if payload.is_expert:
            await self.event_user.identify(
                payload.author_uuid,
                data=dict(
                    type=UserType.AGENT,
                    name=payload.answer.author.name,
                    avatar=dict(
                        image=payload.answer.author.avatar
                        if payload.answer.author.avatar
                        else None,
                        crop=to_dict(self.avatar.crop),
                    ),
                ),
            )
        elif payload.is_system:
            await self.event_user.identify(
                UserType.SYSTEM, data=dict(type=UserType.SYSTEM)
            )
        else:
            await self.event_user.identify(payload.author_uuid)

        pub_entries = list()
        if payload.is_expert_say:
            # special case: expert say
            text = payload.answer.comment.text
            if text.startswith(self.agent_command_prefix):
                pub_entries.append(AgentCommandEvent(text=text))
            else:
                pub_entries.append(SayEvent(text=text))

        if payload.is_conversation_terminated:
            await self.thread.unlink()
            self.thread.mode = DirectlyThreadMode.BOT

        # put directly event on event ledger
        from meya.directly.event.webhook import DirectlyWebhookEvent

        pub_entries.append(DirectlyWebhookEvent(payload=payload))

        return self.respond(
            *pub_entries,
            status=HTTPStatus.OK,
            data=self.RxResponse(ok=True, accepted=True),
        )

    async def tx(self) -> List[Entry]:
        conversation_id = await self.thread.try_reverse_lookup()
        if not conversation_id:
            return []

        user_ref_id = await self.user.reverse_lookup()
        use_prefix = self.event_user.id != self.user.id

        await self.api.conversation_message(
            text=self.get_transcript_line(
                self.event, self.event_user, use_prefix
            ),
            conversation_id=conversation_id,
            user_ref_id=user_ref_id,
        )

        return []

    @property
    def api(self) -> DirectlyApi:
        return self.get_api()

    def get_api(self, version: ApiVersion = ApiVersion.V2) -> DirectlyApi:
        return DirectlyApi(
            domain=self.domain,
            client_id=self.client_id,
            client_secret=self.client_secret,
            version=version,
            timeout=self.api_timeout,
        )


class DirectlyIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = DirectlyIntegration
