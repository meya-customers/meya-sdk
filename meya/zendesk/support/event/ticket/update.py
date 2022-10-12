from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet


@dataclass
class ZendeskSupportTicketUpdateEvent(WebhookEvent):
    old_ticket: ZendeskSupportTicketGet = entry_field(sensitive=True)
    ticket: ZendeskSupportTicketGet = entry_field(sensitive=True)
