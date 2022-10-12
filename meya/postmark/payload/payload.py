from dataclasses import dataclass
from enum import Enum
from meya.email import Recipient
from typing import List
from typing import Optional


@dataclass
class Header:
    Name: str
    Value: str


@dataclass
class Attachment:
    Name: str
    Content: str
    ContentType: str
    ContentID: str = None


class TrackLinks(Enum):
    NONE = "None"
    HTML_AND_TEXT = "HtmlAndText"
    HTML_ONLY = "HtmlOnly"
    TEXT_ONLY = "TextOnly"


@dataclass
class Email:
    From: str
    To: str
    Cc: Optional[str]
    Bcc: Optional[str]
    Subject: Optional[str]
    Tag: Optional[str]
    HtmlBody: str
    TextBody: str
    ReplyTo: Optional[str]
    Headers: Optional[List[Header]]
    TrackOpens: Optional[bool]
    TrackLinks: Optional[TrackLinks]
    Metadata: Optional[dict]
    Attachments: Optional[List[Attachment]]
    MessageStream: Optional[str]

    @staticmethod
    def comma_delimited_recipients(
        recipients: Optional[List["Recipient"]],
    ) -> Optional[str]:
        return ",".join(Recipient.list_as_text(recipients)) or None

    @staticmethod
    def create_headers(headers: dict) -> List[Header]:
        """
        :param headers: {"key": "val", "foo": "bar"...}
        :return: [Header(Name="key", Value="val"), Header(Name="foo", Value="bar")...]
        """
        return [Header(Name=key, Value=val) for key, val in headers.items()]
