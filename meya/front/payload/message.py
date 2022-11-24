from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.front.payload.teammate import FrontTeammateGet
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from meya.util.form_data import BinaryFile
from numbers import Real
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


"""
https://dev.frontapp.com/reference/messages-1
"""


@dataclass
class FrontBodyFormat(SimpleEnum):
    MARKDOWN = "markdown"
    HTML = "html"


@dataclass
class FrontMessageBaseMetadata(FrontPayload):
    thread_ref: Optional[str] = payload_field(default=None)


@dataclass
class FrontMessageBase(FrontPayload):
    body: str = payload_field()


@dataclass
class FrontMessageGetMetadata(FrontMessageBaseMetadata):
    pass


@dataclass
class FrontMessageGetRecipientRelated:
    contact: Optional[str] = payload_field(default=None)
    conversation: Optional[str] = payload_field(default=None)


@dataclass
class FrontMessageGetRecipientLinks:
    related: FrontMessageGetRecipientRelated = payload_field(
        default_factory=FrontMessageGetRecipientRelated
    )


@dataclass
class FrontMessageGetRecipient(FrontPayload):
    links: FrontMessageGetRecipientLinks = payload_field(
        default_factory=FrontMessageGetRecipientLinks, key="_links"
    )
    handle: str = payload_field()
    role: str = payload_field()


@dataclass
class FrontAttachmentMetadata(FrontPayload):
    is_inline: bool = payload_field()


@dataclass
class FrontAttachment(FrontPayload):
    url: str = payload_field()
    filename: str = payload_field()
    content_type: str = payload_field()
    size: int = payload_field()
    metadata: FrontAttachmentMetadata = payload_field()


@dataclass
class FrontMessageGet(FrontMessageBase):
    author: Optional[FrontTeammateGet] = payload_field(default=None)
    created_at: Real = payload_field()
    metadata: FrontMessageGetMetadata = payload_field(
        default_factory=FrontMessageGetMetadata
    )
    recipients: List[FrontMessageGetRecipient] = payload_field()
    text: str = payload_field()
    type: str = payload_field()


@dataclass
class FrontPartnerChannelMessage(FrontMessageGet):
    id: str = payload_field()
    is_inbound: bool = payload_field()
    links: FrontMessageGetRecipientLinks = payload_field(
        default_factory=FrontMessageGetRecipientLinks, key="_links"
    )
    attachments: Optional[List[FrontAttachment]] = payload_field(
        default_factory=list
    )


@dataclass
class FrontPartnerChannelMetadata(FrontPayload):
    external_conversation_id: Optional[str] = payload_field(default=None)
    external_conversation_ids: List[str] = payload_field(default_factory=list)


@dataclass
class FrontCustomChannelHeaders(FrontPayload):
    in_reply_to: Optional[str] = payload_field(default=None)


@dataclass
class FrontCustomChannelMetadata(FrontPayload):
    headers: Optional[FrontCustomChannelHeaders] = payload_field(default=None)


@dataclass
class FrontMessageReplyOptions(FrontPayload):
    tag_ids: Optional[List[str]] = payload_field(default=None)
    archive: Optional[bool] = payload_field(default=None)


@dataclass
class FrontMessageReply(FrontMessageBase):
    author_id: Optional[str] = payload_field(default=None)
    bcc: Optional[List[str]] = payload_field(default=None)
    cc: Optional[List[str]] = payload_field(default=None)
    options: FrontMessageReplyOptions = payload_field(
        default_factory=FrontMessageReplyOptions
    )
    sender_name: Optional[str] = payload_field(default=None)
    subject: Optional[str] = payload_field(default=None)
    text: Optional[str] = payload_field(default=None)
    to: Optional[List[str]] = payload_field(default=None)
    attachments: Optional[List[BinaryFile]] = payload_field(default=None)


@dataclass
class FrontMessageReceiveSender(FrontPayload):
    contact_id: Optional[str] = payload_field(default=None)
    handle: str = payload_field()
    name: Optional[str] = payload_field(default=None)


@dataclass
class FrontMessageReceiveMetadata(FrontMessageBaseMetadata):
    headers: Optional[Dict[str, str]] = payload_field(default=None)


@dataclass
class FrontMessageReceive(FrontMessageBase):
    body_format: Optional[FrontBodyFormat] = payload_field(default=None)
    metadata: FrontMessageReceiveMetadata = payload_field(
        default_factory=FrontMessageReceiveMetadata
    )
    sender: FrontMessageReceiveSender = payload_field()
    subject: Optional[str] = payload_field(default=None)
    attachments: Optional[List[BinaryFile]] = payload_field(default=None)


@dataclass
class FrontMessageImportMetadata(FrontMessageBaseMetadata):
    is_archived: Optional[bool] = payload_field(default=None)
    is_inbound: bool = payload_field()
    should_skip_rules: Optional[bool] = payload_field(default=None)


@dataclass
class FrontMessageImportSender(FrontPayload):
    author_id: Optional[str] = payload_field(default=None)
    handle: str = payload_field()
    name: Optional[str] = payload_field(default=None)


@dataclass
class FrontMessageImport(FrontMessageBase):
    body_format: Optional[str] = payload_field(default=None)
    created_at: Real = payload_field()
    external_id: str = payload_field()
    metadata: FrontMessageImportMetadata = payload_field()
    sender: FrontMessageImportSender = payload_field()
    subject: Optional[str] = payload_field(default=None)
    to: List[str] = payload_field()
    cc: Optional[List[str]] = payload_field(default=None)
    bcc: Optional[List[str]] = payload_field(default=None)
    type: Optional[str] = payload_field(default=None)


@dataclass
class FrontCommentCreate(FrontMessageBase):
    author_id: str = payload_field()


@dataclass
class FrontMessageDetails(FrontMessageBase):
    id: str = payload_field()
    type: str = payload_field()
    created_at: Real = payload_field()
    links: FrontMessageGetRecipientLinks = payload_field(key="_links")
    is_draft: bool = payload_field()
    text: Optional[str] = payload_field()
    subject: Optional[str] = payload_field()
    metadata: Optional[FrontMessageGetMetadata] = payload_field(default=None)
    author: Optional[FrontTeammateGet] = payload_field(default=None)
    recipients: Optional[List[FrontMessageGetRecipient]] = payload_field(
        default_factory=list
    )
    attachments: Optional[List[FrontAttachment]] = payload_field(
        default_factory=list
    )

    @property
    def conversation_id(self) -> Union[None, str]:
        try:
            return self.links.related.conversation.split("/")[-1]
        except Exception:  # noqa
            return None


@dataclass
class FrontSendIncomingMessageResponse(FrontPayload):
    conversation_reference: str = payload_field()
    message_uid: str = payload_field()
    status: str = payload_field()
    thread_ref: Optional[str] = payload_field(default=None)
