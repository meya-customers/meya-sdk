from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.email import Recipient
from meya.email.component.send import EmailSendComponent
from meya.integration.element.api import ApiComponentResponse
from meya.sendgrid.integration.integration import SendgridIntegrationRef
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


class SendgridComponentError(SimpleEnum):
    INTERNAL = "internal"
    TIMEOUT = "timeout"
    BAD_REQUEST = "bad_request"
    REQUEST_SIZE = "request_size"


@dataclass
class SendgridComponentResponse(ApiComponentResponse):
    status: Optional[int] = response_field(default=None)
    error: Optional[SendgridComponentError] = response_field(default=None)


@dataclass
class SendgridSendComponent(EmailSendComponent):
    integration: SendgridIntegrationRef = element_field(
        help=(
            "Reference path to the Sendgrid integration element to use to "
            "send an email."
        )
    )
    reply_to: Optional[List[Recipient]] = element_field(
        default=None,
        help=(
            "A list of recipients that will be included in the `Reply-To` "
            "header. "
        ),
    )
    attachments: Optional[List[str]] = element_field(
        default=None,
        help=(
            "A list of URLs to files that will be downloaded and attached to"
            "the email. Each file must be less than 10MB. "
            "The MIME type of the file will be determined by the file, but "
            "if the MIME type could not be determined, it will default to "
            "`application/octet-stream`."
        ),
    )
