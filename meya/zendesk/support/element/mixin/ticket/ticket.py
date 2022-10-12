from dataclasses import dataclass
from meya.element.field import element_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from meya.zendesk.support.payload.ticket_field import (
    ZendeskSupportTicketFieldPair,
)
from typing import List
from typing import Optional


# TODO Add Enums for ticket_type and priority
@dataclass
class ZendeskTicketMixin(ZendeskBaseMixin):
    requester_id: Optional[int] = element_field(
        default=None, help="The user who requested this ticket"
    )
    subject: Optional[str] = element_field(
        default=None, help="The value of the subject field for this ticket"
    )
    comment: Optional[str] = element_field(
        default=None, help="Add a comment to the ticket"
    )
    comment_public: Optional[bool] = element_field(
        default=None, help="Controls whether the ticket is public or not"
    )
    tags: Optional[List[str]] = element_field(
        default=None, help="An array of tags to add to the ticket"
    )
    custom_fields: Optional[
        List[ZendeskSupportTicketFieldPair]
    ] = element_field(
        default=None,
        help=(
            "An array of the custom field objects consisting "
            "of IDs and values"
        ),
    )
    ticket_type: Optional[str] = element_field(
        default=None, help="The type of this ticket"
    )
    status: Optional[ZendeskSupportTicketStatus] = element_field(
        default=None, help="The state of the ticket"
    )
    priority: Optional[str] = element_field(
        default=None,
        help="The urgency with which the ticket should be addressed",
    )
    assignee_id: Optional[int] = element_field(
        default=None, help="The agent currently assigned to the ticket"
    )
    group_id: Optional[int] = element_field(default=None)
    external_id: Optional[str] = element_field(default=None)
    ticket_form_id: Optional[int] = element_field(
        default=None, help="The ID of the ticket form to render for the ticket"
    )
    brand_id: Optional[int] = element_field(
        default=None, help="The ID of the brand this ticket is associated with"
    )
