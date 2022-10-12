import re

from bs4 import BeautifulSoup
from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.zendesk.support.payload import ZendeskSupportPayload
from meya.zendesk.support.payload.attachment import ZendeskSupportAttachment
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportTicketCommentBase(ZendeskSupportPayload):
    author_id: int = payload_field()
    body: str = payload_field()
    public: bool = payload_field()


@dataclass
class ZendeskSupportTicketCommentGet(ZendeskSupportTicketCommentBase):
    attachments: List[ZendeskSupportAttachment] = payload_field(
        default_factory=list
    )
    created_at: str = payload_field()
    html_body: str = payload_field()
    id: int = payload_field()

    @property
    def body_with_links(self) -> str:
        soup = BeautifulSoup(self.html_body, "html.parser")
        links = soup.find_all("a", href=True)
        result = self.body
        for link in links:
            text = link.text
            href = link["href"]
            new_result, count = re.subn(
                re.escape(text), f"[{text}]({href})", result
            )
            if count == 1:
                result = new_result
            else:
                result = f"{result}\n\n{href}"
        return result


@dataclass
class ZendeskSupportTicketCommentCreate(ZendeskSupportTicketCommentBase):
    author_id: Optional[int] = payload_field(default=None)
    public: Optional[bool] = payload_field(default=None)
    uploads: Optional[List[str]] = payload_field(default=None)
