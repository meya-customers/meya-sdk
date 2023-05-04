from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef
from meya.zendesk.support.payload.user import ZendeskSupportUserGet
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class ZendeskSupportUserUpdateComponent(BaseApiComponent):
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
        help="The ID of the user to update.",
    )
    name: Optional[str] = element_field(
        default=None,
        help="The user's name.",
    )
    details: Optional[str] = element_field(
        default=None,
        help=(
            "Any details you want to store about the user, such as an address"
        ),
    )
    email: Optional[str] = element_field(
        default=None,
        help=(
            "The user's secondary email address. See the Zendesk "
            "[email address](https://developer.zendesk.com/api-reference/ticketing/users/users/#email-address) "
            "documentation for more information."
        ),
    )
    verified: Optional[bool] = element_field(
        default=None,
        help="Whether any of the user's identities have been verified.",
    )
    phone: Optional[str] = element_field(
        default=None,
        help=(
            "The user's primary phone number. See the Zendesk "
            "[phone number](https://developer.zendesk.com/api-reference/ticketing/users/users/#phone-number) "
            "documentation for more information."
        ),
    )
    tags: Optional[List[str]] = element_field(
        default=None,
        help=(
            "An array of tags to add to the user. This is only present if "
            "user tagging is enabled for your Zendesk instance."
        ),
    )
    user_fields: Optional[Dict[str, Any]] = element_field(
        default=None,
        help=(
            "Values of custom fields in the user's profile. See the Zendesk "
            "[user fields](https://developer.zendesk.com/api-reference/ticketing/users/users/#user-fields) "
            "documentation for more information."
        ),
    )
    external_id: Optional[str] = element_field(
        default=None,
        help=(
            "An ID you can use to link Zendesk Support users to local "
            "records. Note, the Zendesk API treats the ID as case sensitive."
        ),
    )
