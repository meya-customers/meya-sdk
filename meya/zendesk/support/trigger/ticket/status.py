from dataclasses import dataclass
from meya.element.field import element_field
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from meya.zendesk.support.trigger.ticket.update import (
    ZendeskSupportTicketUpdateTrigger,
)


@dataclass
class ZendeskSupportTicketStatusTrigger(ZendeskSupportTicketUpdateTrigger):
    status: ZendeskSupportTicketStatus = element_field(default=None)
