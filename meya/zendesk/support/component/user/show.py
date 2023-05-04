from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import Optional


@dataclass
class ZendeskSupportUserShowComponent(BaseApiComponent):
    @dataclass
    class Response:
        result: ZendeskSupportUserGet = response_field(sensitive=True)

    integration: ZendeskSupportIntegrationRef = element_field(
        help=(
            "The reference path to the Zendesk Support integration file. "
            "See the [integration reference paths](https://docs.meya.ai/docs/integrations-1#integration-reference-paths) "
            "documentation for more information."
        ),
    )
    user_id: Optional[int] = element_field(
        default=None,
        help=(
            "The ID of the user to show. If this is not set, the component "
            "will attempt to resolve the user ID from the current Meya "
            "thread."
        ),
    )
    bot_agent: bool = element_field(
        default=False,
        help=(
            "If set, the component will show the Zendesk bot agent user that "
            "is associated with the API token used in the integration."
        ),
    )
