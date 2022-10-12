from dataclasses import dataclass
from meya.element.field import element_field
from meya.email.component.send import EmailSendComponent
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.postmark.integration import PostmarkIntegration
from meya.postmark.integration import PostmarkIntegrationRef
from meya.postmark.integration.api import PostmarkApi
from meya.postmark.payload.payload import Attachment as ApiAttachment
from meya.postmark.payload.payload import Email
from meya.postmark.payload.payload import TrackLinks
from typing import List
from typing import Optional


@dataclass
class Attachment:
    """
    ApiAttachment is CamelCase, whereas BFML should be snake_case
    TODO: consider a to_dict() native solution instead
    """

    name: str
    content: str
    content_type: str
    content_id: str = None

    def as_api_attachment(self) -> ApiAttachment:
        return ApiAttachment(
            Name=self.name,
            Content=self.content,
            ContentType=self.content_type,
            ContentID=self.content_id,
        )


@dataclass
class PostmarkSendComponent(EmailSendComponent):
    """
    Learn more: https://postmarkapp.com/developer/api/email-api#send-a-single-email
    """

    integration: PostmarkIntegrationRef = element_field()

    # Postmark specific fields
    tag: Optional[str] = element_field(default=None)
    reply_to: Optional[str] = element_field(default=None)
    track_opens: Optional[bool] = element_field(default=None)
    track_links: Optional[TrackLinks] = element_field(default=None)
    metadata: Optional[dict] = element_field(default=None)
    attachments: Optional[List[Attachment]] = element_field(default=None)
    message_stream: Optional[str] = element_field(default=None)

    async def send(self) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        if self.attachments is None:
            attachments = None
        else:
            attachments = [
                attachment.as_api_attachment()
                for attachment in self.attachments
            ]
        integration: PostmarkIntegration = await self.resolve(self.integration)
        email = Email(
            From=self.from_.as_text,
            To=Email.comma_delimited_recipients(self.to),
            Cc=Email.comma_delimited_recipients(self.cc),
            Bcc=Email.comma_delimited_recipients(self.bcc),
            Subject=self.subject,
            Tag=self.tag,
            HtmlBody=self.html,
            TextBody=self.text,
            ReplyTo=self.reply_to,
            Headers=Email.create_headers(self.headers)
            if self.headers
            else None,
            TrackOpens=self.track_opens,
            TrackLinks=self.track_links,
            Metadata=self.metadata,
            Attachments=attachments,
            MessageStream=self.message_stream,
        )
        return await PostmarkApi(server_token=integration.server_token).send(
            email, wait_for_response=self.wait_for_response
        )
