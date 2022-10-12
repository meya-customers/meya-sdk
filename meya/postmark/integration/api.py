import os

from dataclasses import dataclass
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.postmark.payload.payload import Email
from meya.util.dict import to_dict
from typing import Optional

API_ROOT = "https://api.postmarkapp.com"


@dataclass
class PostmarkApi(Api):
    server_token: str
    api_root: str = API_ROOT

    async def send(
        self, email: Email, wait_for_response: bool = True
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        req = self.http.make_request_entry(
            method="POST",
            url=os.path.join(self.api_root, "email"),
            headers=self._get_headers(),
            json=to_dict(email),
        )

        if wait_for_response:
            return req, await self.http.send(req)
        else:
            return req, None

    def _get_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": self.server_token,
        }
