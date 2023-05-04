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
        default=None, help="The user who requested this ticket."
    )
    subject: Optional[str] = element_field(
        default=None, help="The value of the subject field for this ticket."
    )
    comment: Optional[str] = element_field(
        default=None, help="Add a comment to the ticket."
    )
    comment_attachments: Optional[List[str]] = element_field(
        default=None,
        help=(
            "A list of file URLs to attach to the comment. These files"
            "will be downloaded from the source and then uploaded to Zendesk "
            "to ensure they are secured by Zendesk's security policies and "
            "user access rights.\n\n"
            "Be careful not to attach too many large files that take long "
            "to download and upload, as this could exceed the component "
            "timeout and cause the component to fail.\n\n"
            "If any file fails to download or upload, the component will log "
            "the exception in your app's logs.\n\n"
            "The file size limit is 50MB per attachment.\n\n"
            "There is a 10s timeout per file download and a 10s "
            "timeout per file upload."
        ),
    )
    comment_public: Optional[bool] = element_field(
        default=None, help="Controls whether the ticket is public or not."
    )
    tags: Optional[List[str]] = element_field(
        default=None, help="An array of tags to add to the ticket."
    )
    custom_fields: Optional[
        List[ZendeskSupportTicketFieldPair]
    ] = element_field(
        default=None,
        help=(
            "An array of the custom field objects consisting "
            "of IDs and values."
        ),
    )
    ticket_type: Optional[str] = element_field(
        default=None,
        help=(
            "The type of this ticket. Allowed values are `problem`, "
            "`incident`, `question`, or `task`."
        ),
    )
    status: Optional[ZendeskSupportTicketStatus] = element_field(
        default=None,
        help=(
            "The state of the ticket. Allowed values are `new`, `open`, "
            "`pending`, `hold`, `solved`, or `closed`."
        ),
    )
    priority: Optional[str] = element_field(
        default=None,
        help=(
            "The urgency with which the ticket should be addressed. "
            "Allowed values are `urgent`, `high`, `normal`, or `low`."
        ),
    )
    assignee_id: Optional[int] = element_field(
        default=None, help="The agent currently assigned to the ticket."
    )
    group_id: Optional[int] = element_field(default=None)
    external_id: Optional[str] = element_field(
        default=None,
        help=(
            "An ID you can use to link Zendesk Support tickets to local "
            "records."
        ),
    )
    ticket_form_id: Optional[int] = element_field(
        default=None,
        help="The ID of the ticket form to render for the ticket.",
    )
    brand_id: Optional[int] = element_field(
        default=None,
        help="The ID of the brand this ticket is associated with.",
    )
