from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from typing import Optional


@dataclass
class ZendeskSupportTicketShowComponent(BaseApiComponent, ZendeskBaseMixin):
    """
    This component will query the Zendesk Support API for a ticket and return
    the ticket API response payload.
    """

    @dataclass
    class Response:
        result: ZendeskSupportTicketGet = response_field(sensitive=True)

    ticket_id: Optional[int] = element_field(
        default=None,
        help="The ID of the ticket to show.",
    )
