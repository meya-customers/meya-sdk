from dataclasses import dataclass
from http import HTTPStatus
from meya.directly.component.api import DirectlyApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse


@dataclass
class AutomateMessage(ApiComponentResponse):
    answer_uuid: str = response_field()
    text: str = response_field()

    @classmethod
    def create(cls, res: HttpResponseEntry) -> "AutomateMessage":
        ok = res.status == HTTPStatus.OK
        kwargs = {}
        if ok:
            kwargs = {
                "answer_uuid": res.data["messageId"],
                "text": res.data["text"],
            }
        return cls(result=res.data, status=res.status, ok=ok, **kwargs)


@dataclass
class DirectlyAutomateMessageComponent(DirectlyApiComponent):
    text: str = element_field()

    @dataclass
    class Response(AutomateMessage):
        pass

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.automate_post_message(text=self.text)

    def create_response(self, res: HttpResponseEntry) -> AutomateMessage:
        return AutomateMessage.create(res)
