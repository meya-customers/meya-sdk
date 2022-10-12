import os

from dataclasses import dataclass
from meya.db.view.http import HttpBasicAuth
from meya.email import Recipient
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from typing import List
from typing import Optional

API_ROOT = "https://api.mailgun.net/v3"


@dataclass
class MailgunApi(Api):
    api_key: str
    domain: str
    api_root: str = API_ROOT

    async def send(
        self,
        from_: Recipient,
        to: List[Recipient],
        cc: List[Recipient] = None,
        bcc: List[Recipient] = None,
        subject: str = None,
        text: str = None,
        html: str = None,
        headers: dict = None,
        wait_for_response: bool = True,
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        data = {
            "from": from_.as_text,
            "to": Recipient.list_as_text(to),
            "cc": Recipient.list_as_text(cc),
            "bcc": Recipient.list_as_text(bcc),
            "subject": subject or "",
        }
        if text is not None:
            data["text"] = text
        if html is not None:
            data["html"] = html
        if headers is not None:
            data.update(self.convert_headers(headers))

        req = self.http.make_request_entry(
            method="POST",
            url=os.path.join(self.api_root, self.domain, "messages"),
            auth=self.auth,
            data=data,
        )

        if wait_for_response:
            return req, await self.http.send(req)
        else:
            return req, None

    @staticmethod
    def convert_headers(headers: dict) -> dict:
        """
        :param headers: {"key": "val", "foo": "bar"...}
        :return: {"h:key": "val", "h:foo": "bar"...}
        """
        return {f"h:{key}": val for key, val in headers.items()}

    @property
    def auth(self) -> HttpBasicAuth:
        return HttpBasicAuth("api", self.api_key)
