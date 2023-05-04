from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.element.mixin.base import ZendeskBaseMixin
from meya.zendesk.support.payload.sort import ZendeskSupportSortOrder
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportTicketSearchComponent(BaseApiComponent, ZendeskBaseMixin):
    """
    This component searches for tickets in Zendesk Support based on a query.

    Here is an example of a flow that searches for tickets based on the user's
    ID and displays the IDs of all the tickets:

    ```yaml
    triggers:
      - keyword: zendesk_support_ticket_search

    steps:
      - type: meya.zendesk.support.component.user.show
        integration: integration.zendesk.support
      - type: meya.zendesk.support.component.ticket.search
        integration: integration.zendesk.support
        query:
          - requester_id:(@ flow.result.id )
      - ask: Your tickets are (@ flow.result | map(attribute="id") | join(", ") )
    ```
    """

    @dataclass
    class Response:
        result: List[ZendeskSupportTicketGet] = response_field(sensitive=True)
        count: int = response_field()

    query: List[str] = element_field(
        help=(
            "The query to search for tickets. This must be a valid search "
            "query based on the Zendesk search syntax. See the Zendesk search "
            "[reference guide](https://support.zendesk.com/hc/en-us/articles/4408886879258) "
            "for more information."
        ),
    )
    sort_by: Optional[str] = element_field(
        default=None,
        help=(
            "The field to sort the results by. This can be one of "
            "`updated_at`, `created_at`, `priority`, `status`, or "
            "`ticket_type`. Defaults to sorting by relevance."
        ),
    )
    sort_order: Optional[ZendeskSupportSortOrder] = element_field(
        default=None,
        help=(
            "The sort order of the results. This can be `asc` or `desc`. "
            "Defaults to `desc`."
        ),
    )
