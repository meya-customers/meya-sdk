from dataclasses import dataclass
from http import HTTPStatus
from meya.component.element.base_api import BaseApiComponent
from meya.db.view.http import HttpTimeoutError
from meya.element.field import meta_field
from meya.entry import Entry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse
from typing import ClassVar
from typing import List
from typing import Set


@dataclass
class ApiComponent(BaseApiComponent):
    """
    Useful component abstraction for making web API calls
    """

    ok_status: ClassVar[Set[int]] = {HTTPStatus.OK}

    is_abstract: bool = meta_field(value=True)

    @dataclass
    class Response(ApiComponentResponse):
        pass

    async def start(self) -> List[Entry]:
        try:
            res = await self.make_request()
            response = self.create_response(res)
        except HttpTimeoutError:
            response = self.Response.create_timeout()
        await self.on_response(response)
        return self.respond(data=response)

    async def make_request(self) -> HttpResponseEntry:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    def create_response(self, res: HttpResponseEntry) -> ApiComponentResponse:
        """Override in sub-class for custom behavior"""
        return self.Response(
            result=res.data, status=res.status, ok=res.status in self.ok_status
        )

    async def on_response(self, response: ApiComponentResponse):
        """Override in sub-class for custom callback behavior"""
        pass
