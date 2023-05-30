from dataclasses import dataclass
from http import HTTPStatus
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.email import Recipient
from meya.entry import Entry
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element import IntegrationRef
from meya.integration.element.api import ApiComponentResponse
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Set


@dataclass
class EmailSendComponent(BaseApiComponent):
    is_abstract: bool = meta_field(value=True)

    from_: Recipient = element_field(
        help=(
            "The sender of the email. Depending on the integration, this "
            "might need to be a verified email address."
        )
    )
    to: List[Recipient] = element_field(
        help="A list of recipients that will receive the email."
    )
    cc: List[Recipient] = element_field(
        default_factory=list,
        help=("A list of recipients that will receive a copy of the email."),
    )
    bcc: List[Recipient] = element_field(
        default_factory=list,
        help=(
            "A list of recipients that will receive a blind copy of the email."
        ),
    )
    subject: Optional[str] = element_field(
        default=None, help="The subject of the email."
    )
    text: Optional[str] = element_field(
        default=None,
        help=(
            "The text body of the email. Text bodies are supported by all "
            "email clients, and is the fallback if the email client does not "
            "support HTML. We recommend that you always include a text body "
            "in your emails."
        ),
    )
    html: Optional[str] = element_field(
        default=None,
        help=(
            "The HTML body of the email. Not all email clients support HTML, "
            "so you should always include a text body as a fallback."
        ),
    )
    headers: Optional[dict] = element_field(
        default=None,
        help="A dictionary of custom email headers to include in the email.",
    )
    wait_for_response: bool = element_field(
        default=True,
        help=(
            "If `true`, the component will wait for a response from the "
            "integration. If `false`, the component will not wait for a "
            "response from the integration and the email will be sent "
            "asynchronously. In this case a send failure will only be "
            "reported in your app logs and not to the user."
        ),
    )
    integration: IntegrationRef = element_field(
        help=(
            "Reference path to the integration element to use to send an "
            "email."
        )
    )

    ok_status: ClassVar[Set[int]] = {HTTPStatus.OK}

    def validate(self):
        super().validate()
        if not (self.text or self.html):
            raise self.validation_error(
                "Either one of `text` or `html` is required."
            )

    async def send(self) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    async def start(self) -> List[Entry]:
        req, res = await self.send()
        if res:
            entries = []
            response = ApiComponentResponse(
                result=res.data,
                status=res.status,
                ok=res.status in self.ok_status,
            )
        else:
            entries = [req]
            response = {}
        return self.respond(*entries, data=response)
