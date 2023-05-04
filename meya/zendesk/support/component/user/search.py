from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.sort import ZendeskSupportSortOrder
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportUserSearchComponent(BaseApiComponent):
    """
    This will search for users in Zendesk Support and return the user API
    response payload.

    ```yaml
    triggers:
      - keyword: zendesk_support_user_search

    steps:
      - say: What is the user's email?
      - type: email_address_input
        required: true
      - type: meya.zendesk.support.component.user.search
        integration: integration.zendesk.support
        query:
          - email:(@ flow.result )
      - say: Users found are (@ flow.result )
    ```
    """

    @dataclass
    class Response:
        result: List[ZendeskSupportUserGet] = response_field(sensitive=True)
        count: int = response_field()

    integration: ZendeskSupportIntegrationRef = element_field(
        help=(
            "The reference path to the Zendesk Support integration file. "
            "See the [integration reference paths](https://docs.meya.ai/docs/integrations-1#integration-reference-paths) "
            "documentation for more information."
        ),
    )
    query: List[str] = element_field(
        help=(
            "The query to search for users. This must be a valid search "
            "query based on the Zendesk search syntax. See the Zendesk search "
            "[reference guide](https://support.zendesk.com/hc/en-us/articles/4408886879258) "
            "for more information."
        ),
    )
    sort_by: Optional[str] = element_field(
        default=None,
        help="The field to sort the results by.",
    )
    sort_order: Optional[ZendeskSupportSortOrder] = element_field(
        default=None,
        help=(
            "The sort order of the results. This can be `asc` or `desc`. "
            "Defaults to `desc`."
        ),
    )
