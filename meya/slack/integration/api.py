from dataclasses import dataclass
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from typing import List
from typing import Optional


@dataclass
class SlackApi(Api):
    webhook_url: str

    async def send(
        self,
        text: Optional[str] = None,
        blocks: Optional[List[dict]] = None,
        wait_for_response: bool = True,
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        data = dict()
        if text:
            data["text"] = text
        if blocks:
            data["blocks"] = blocks

        req = self.http.make_request_entry(
            method="POST", url=self.webhook_url, json=data
        )

        if wait_for_response:
            return req, await self.http.send(req)
        else:
            return req, None
