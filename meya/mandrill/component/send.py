from dataclasses import dataclass
from meya.element.field import element_field
from meya.email.component.send import EmailSendComponent
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.mandrill.integration import MandrillIntegration
from meya.mandrill.integration import MandrillIntegrationRef
from meya.mandrill.integration.api import MandrillApi
from meya.mandrill.payload.payload import MandrillRecipient
from meya.mandrill.payload.payload import RecipientType
from typing import List
from typing import Optional


@dataclass
class MandrillSendComponent(EmailSendComponent):
    """
    Learn more: https://mandrillapp.com/api/docs/messages.JSON.html#method=send
    """

    integration: MandrillIntegrationRef = element_field()

    async def send(self) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        integration: MandrillIntegration = await self.resolve(self.integration)
        return await MandrillApi(api_key=integration.api_key).send(
            from_=self.from_,
            recipients=self.get_recipients(),
            subject=self.subject,
            text=self.text,
            html=self.get_html(),
            headers=self.headers,
            wait_for_response=self.wait_for_response,
        )

    def get_recipients(self) -> List[MandrillRecipient]:
        return [
            *[
                MandrillRecipient(
                    recipient.email, recipient.name, RecipientType.TO
                )
                for recipient in self.to
            ],
            *[
                MandrillRecipient(
                    recipient.email, recipient.name, RecipientType.CC
                )
                for recipient in self.cc
            ],
            *[
                MandrillRecipient(
                    recipient.email, recipient.name, RecipientType.BCC
                )
                for recipient in self.bcc
            ],
        ]

    def get_html(self) -> str:
        if self.html:
            return self.html
        else:
            return f"<p>{self.text}</p>"
