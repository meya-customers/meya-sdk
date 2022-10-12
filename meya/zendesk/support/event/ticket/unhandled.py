from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.user import ZendeskSupportUserGet


@dataclass
class ZendeskSupportTicketUnhandledEvent(WebhookEvent):
    ticket: ZendeskSupportTicketGet = entry_field(sensitive=True)
    current_user: ZendeskSupportUserGet = entry_field(sensitive=True)
    requester: ZendeskSupportUserGet = entry_field(sensitive=True)
