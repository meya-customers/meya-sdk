from dataclasses import dataclass
from meya.csp.integration import CspIntegration
from meya.csp.integration.integration import CspIntegrationFilter
from meya.db.view.thread import ThreadMode
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.gridql.parser import GridQL
from meya.gridql.parser import QueryException
from meya.integration.element.element import FilterElementSpecUnion
from meya.zendesk.base.integration import ZendeskBaseIntegration
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from numbers import Real
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type
from typing import Union


@dataclass
class ZendeskSupportIntegrationFilter(CspIntegrationFilter):
    rx_unhandled_ticket: FilterElementSpecUnion = element_field(default=False)

    def is_valid(self) -> (bool, Optional[str]):
        """
        :return: True, None if valid, False, "error message" otherwise
        """
        tests = (("rx_unhandled_ticket", self.rx_sub),)
        for name, value in tests:
            if not isinstance(value, bool):
                try:
                    # try parse and match to validate the input
                    gridql = GridQL.create(value)
                    gridql.match(
                        dict(ticket={}, current_user={}, requester={})
                    )
                except QueryException as e:
                    return (
                        False,
                        f"Invalid GridQL for `{name}` field with value `{value}`: {str(e)}",
                    )
        return super().is_valid()

    @staticmethod
    def does_match_unhandled_ticket(
        ticket: ZendeskSupportTicketGet,
        current_user: ZendeskSupportUserGet,
        requester: ZendeskSupportUserGet,
        field: FilterElementSpecUnion,
    ) -> bool:
        """
        :return: true|false whether or not to continue processing
        """
        if isinstance(field, bool):
            return field
        else:
            # Lucene style match
            return GridQL.create(field).match(
                dict(
                    ticket=ticket.to_dict(),
                    current_user=current_user.to_dict(),
                    requester=requester.to_dict(),
                )
            )


@dataclass
class ZendeskSupportIntegration(ZendeskBaseIntegration, CspIntegration):
    """
    # Install instructions

    ## API token
    https://SUBDOMAIN.zendesk.com/agent/admin/api/settings

    - Log in with the bot agent email
    - Create the bot agent API token

    ## HTTP target
    https://SUBDOMAIN.zendesk.com/agent/admin/extensions

    - Create a new HTTP target (note the name for the Trigger step below)
    - Use your webhook URL. (Found via `meya webhooks` command)
    - Method POST
    - Username "meya"
    - Generate and use your own target password
    - Test target using JSON body: {"test": "RANDOM_STRING"}
    - You should receive a 200 response and "message": "Zendesk Support HTTP target success!"
    - Note: for subsequent tests change the value of RANDOM_STRING to avoid cached responses
    - If successful, create the target

    ## Trigger
    https://SUBDOMAIN.zendesk.com/agent/admin/triggers

    - Create a new Trigger
    - Add two "ANY" conditions: "Ticket is Created" and "Ticket
    is Updated"
    - Add an Action "Notify target" pointing to your new HTTP target

    Use this JSON body:

    ```json
    {
        "ticket_id": "{{ticket.id}}",
        "updated_at": "{{ticket.updated_at_with_timestamp}}",
        "current_user_id": "{{current_user.id}}"
    }
    ```
    """

    NAME: ClassVar[str] = "zendesk_support"

    target_password: str = element_field(
        help=(
            "The target password you generated. This is used by the "
            "integration to authenticate incoming Zendesk Support webhooks."
        )
    )
    auto_reopen_ticket: Union[bool, ThreadMode] = element_field(
        default=ThreadMode.AGENT,
        help=(
            "This automatically reopens the linked ticket, if the ticket is "
            "in either the 'pending', 'hold' or 'solved' state, and the "
            "user sends a new event e.g. a say event or an image event. "
            "This setting can either be 'True/False' or it can be a specific "
            "thread mode, so when the thread enters this mode and the user "
            "sends a new event, then the linked ticket will be reopened."
        ),
    )
    unlink_ticket_status: List[ZendeskSupportTicketStatus] = element_field(
        default_factory=lambda: [ZendeskSupportTicketStatus.CLOSED],
        help=(
            "The set of Zendesk Support ticket statuses that will unlink the "
            "Meya thread from the ticket. When the Meya thread is unlinked, "
            "then the integration will no longer send events to Zendesk "
            "Support."
        ),
    )
    extract_html_links: bool = element_field(
        default=True,
        help=(
            "This will cause the integration to parse out any hyperlinks in "
            "an incoming ticket comment, and convert it to a markdown link "
            "that can be rendered by messaging integrations such as Orb or "
            "Zendesk Sunshine Conversations."
        ),
    )
    include_text_with_media: bool = element_field(
        default=False,
        help=(
            "When set to 'True' the integration will create a Meya media "
            "event and use the ticket's comment as the media event's text "
            "when the comment has an attachment. When set to 'False' the "
            "comment text will appear as a separate Meya say event. This "
            "setting is only applicable for ticket comments that have an "
            "attachment e.g. an image or a file."
        ),
    )
    upload_attachments: bool = element_field(
        default=True,
        help=(
            "When set to 'True' the integration will upload all Meya media "
            "event files to your Zendesk Support instance instead of keeping "
            "it on the Meya CDN."
        ),
    )
    filter: ZendeskSupportIntegrationFilter = element_field(
        default_factory=ZendeskSupportIntegrationFilter,
        help=(
            "This allows you to specify any valid GridQL query to filter "
            "incoming requests/events and outgoing requests/events."
        ),
    )

    api_timeout: Real = element_field(
        default=5,
        help=(
            "The time, in seconds, to wait for a response from the Zendesk "
            "Support API."
        ),
    )

    def validate(self):
        super().validate()
        if ZendeskSupportTicketStatus.CLOSED not in self.unlink_ticket_status:
            raise self.validation_error(
                "Tickets must be unlinked once closed."
            )


class ZendeskSupportIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = ZendeskSupportIntegration
