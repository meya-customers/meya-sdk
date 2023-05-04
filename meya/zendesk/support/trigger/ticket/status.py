from dataclasses import dataclass
from meya.element.field import element_field
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from meya.zendesk.support.trigger.ticket.update import (
    ZendeskSupportTicketUpdateTrigger,
)


@dataclass
class ZendeskSupportTicketStatusTrigger(ZendeskSupportTicketUpdateTrigger):
    """
    This trigger will match the status of the incoming Zendesk Support
    ticket webhook. For example, this is particularly useful if you would
    like to run a flow when a ticket is `closed`, and you would like to get
    some feedback from the user through a survey or a CSAT score.
    """

    status: ZendeskSupportTicketStatus = element_field(
        default=None,
        help=(
            "The status of the ticket to match. This can be one of `new`, "
            "`open`, `pending`, `hold`, `solved`, or `closed`."
        ),
    )
