from dataclasses import dataclass
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.zendesk.support.event.ticket.unhandled import (
    ZendeskSupportTicketUnhandledEvent,
)
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.user import ZendeskSupportUserGet


@dataclass
class ZendeskSupportTicketUnhandledTrigger(WebhookTrigger):
    """
    This is a special trigger that will match any incoming Zendesk Support
    webhooks that are not linked to a specific Meya thread and user, thereby
    being "unhandled".

    This trigger is particularly useful if you would like to send agent
    initiated messages to the user where the user has not actively requested
    a support agent. Check the [agent-initiated conversations guide](https://docs.meya.ai/docs/sending-agent-initiated-conversations-with-zendesk-support-and-zendesk-sunshine-conversations)
    for more information.
    """

    entry: ZendeskSupportTicketUnhandledEvent = process_field()
    encrypted_entry: ZendeskSupportTicketUnhandledEvent = process_field()

    @dataclass
    class Response:
        ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
        current_user: ZendeskSupportUserGet = response_field(sensitive=True)
        requester: ZendeskSupportUserGet = response_field(sensitive=True)
