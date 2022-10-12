from dataclasses import dataclass
from meya.element.field import element_field
from meya.email.component.send import EmailSendComponent
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.mailgun.integration import MailgunIntegration
from meya.mailgun.integration import MailgunIntegrationRef
from meya.mailgun.integration.api import MailgunApi
from typing import Optional


@dataclass
class MailgunSendComponent(EmailSendComponent):
    """
    Send a transactional email using Mailgun.

    Learn more: https://documentation.mailgun.com/en/latest/api-sending.html#sending
    """

    integration: MailgunIntegrationRef = element_field()

    async def send(self) -> (HttpRequestEntry, Optional[HttpResponseEntry]):
        integration: MailgunIntegration = await self.resolve(self.integration)
        return await MailgunApi(
            api_key=integration.api_key, domain=integration.domain
        ).send(
            from_=self.from_,
            to=self.to,
            cc=self.cc,
            bcc=self.bcc,
            subject=self.subject,
            text=self.text,
            html=self.html,
            headers=self.headers,
            wait_for_response=self.wait_for_response,
        )
