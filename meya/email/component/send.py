from dataclasses import dataclass
from http import HTTPStatus
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.email import Recipient
from meya.entry import Entry
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element import IntegrationRef
from meya.integration.element.api import ApiComponentResponse
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set


@dataclass
class EmailSendComponent(BaseApiComponent):
    is_abstract: bool = meta_field(value=True)

    from_: Recipient = element_field()
    to: List[Recipient] = element_field()
    cc: List[Recipient] = element_field(default_factory=list)
    bcc: List[Recipient] = element_field(default_factory=list)
    subject: Optional[str] = element_field(default=None)
    text: Optional[str] = element_field(default=None)
    html: Optional[str] = element_field(default=None)
    headers: Optional[dict] = element_field(default=None)
    wait_for_response: bool = element_field(default=True)
    integration: IntegrationRef = element_field()

    ok_status: ClassVar[Set[int]] = {HTTPStatus.OK}

    def validate(self):
        super().validate()
        if not (self.text or self.html):
            raise self.validation_error(f"`text` or `html` are required.")

    async def send(self) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    async def start(self) -> List[Entry]:
        req, res = await self.send()
        if res:
            entries = []
            response = ApiComponentResponse(
                result=res.data,
                status=res.status,
                ok=res.status in self.ok_status,
            )
        else:
            entries = [req]
            response = {}
        return self.respond(*entries, data=response)
