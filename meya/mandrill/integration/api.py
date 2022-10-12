import os

from dataclasses import dataclass
from meya.email import Recipient
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from meya.mandrill.payload.payload import MandrillRecipient
from meya.mandrill.payload.payload import Message
from meya.mandrill.payload.payload import Payload
from meya.util.dict import to_dict
from typing import List
from typing import Optional

API_ROOT = "https://mandrillapp.com/api/1.0"


@dataclass
class MandrillApi(Api):
    api_key: str
    api_root: str = API_ROOT

    async def send(
        self,
        from_: Recipient,
        recipients: List[MandrillRecipient],
        html: str,
        subject: Optional[str] = None,
        text: Optional[str] = None,
        headers: Optional[dict] = None,
        wait_for_response: bool = True,
    ) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        payload = Payload(
            key=self.api_key,
            message=Message(
                from_email=from_.email,
                from_name=from_.name,
                to=recipients,
                subject=subject,
                html=html,
                text=text,
                headers=headers,
            ),
        )
        req = self.http.make_request_entry(
            method="POST",
            url=os.path.join(self.api_root, "messages/send.json"),
            json=to_dict(payload),
        )

        if wait_for_response:
            return req, await self.http.send(req)
        else:
            return req, None
