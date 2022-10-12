from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Optional


class RecipientType(Enum):
    TO = "to"
    CC = "cc"
    BCC = "bcc"


@dataclass
class MandrillRecipient:
    email: str
    name: str = None
    type: Enum = RecipientType.TO


@dataclass
class Message:
    from_email: str
    from_name: Optional[str]
    to: List[MandrillRecipient]
    subject: str
    html: str
    text: Optional[str]
    headers: Optional[dict]


@dataclass
class Payload:
    key: str
    message: Message
