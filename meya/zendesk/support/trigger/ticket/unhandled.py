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
    entry: ZendeskSupportTicketUnhandledEvent = process_field()
    encrypted_entry: ZendeskSupportTicketUnhandledEvent = process_field()

    @dataclass
    class Response:
        ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
        current_user: ZendeskSupportUserGet = response_field(sensitive=True)
        requester: ZendeskSupportUserGet = response_field(sensitive=True)
