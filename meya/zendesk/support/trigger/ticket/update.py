from dataclasses import dataclass
from meya.element.field import process_field
from meya.element.field import response_field
from meya.http.trigger import WebhookTrigger
from meya.zendesk.support.event.ticket.update import (
    ZendeskSupportTicketUpdateEvent,
)
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet


@dataclass
class ZendeskSupportTicketUpdateTrigger(WebhookTrigger):
    entry: ZendeskSupportTicketUpdateEvent = process_field()
    encrypted_entry: ZendeskSupportTicketUpdateEvent = process_field()

    @dataclass
    class Response:
        ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
        old_ticket: ZendeskSupportTicketGet = response_field(sensitive=True)
