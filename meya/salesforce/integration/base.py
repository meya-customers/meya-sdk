from dataclasses import dataclass
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from typing import ClassVar
from typing import Type


@dataclass
class SalesforceBaseIntegration:
    """
    Salesforce Access Token documentation:
    https://developer.salesforce.com/docs/atlas.en-us.api_iot.meta/api_iot/qs_auth_access_token.htm
    """

    instance_base_url: str = element_field(
        help=(
            "Your Salesforce instance's base URL with no trailing `/`, "
            "e.g. https://your-instance.salesforce.com"
        )
    )

    client_id: str = element_field(
        help=(
            "This field is called `Consumer Key` in the Salesforce Admin "
            "console and `client_id` in the Auth Api request."
            "The `Consumer Key` can be found at "
            "Salesforce > Build > Create > Apps > Your app."
        )
    )
    client_secret: str = element_field(
        help=(
            "This field is called `Consumer Secret` in the Salesforce Admin "
            "console and `client_secret` in the Auth Api request."
            "The `Consumer Secret` can be found at "
            "Salesforce > Build > Create > Apps > Your app."
        )
    )
    username: str = element_field(
        help=(
            "The email of a valid user in your Salesforce instance. "
            "Usually you would create a dedicated user for app integrations."
        )
    )
    password: str = element_field(
        help=(
            "The password of the user you use to login to your Salesforce "
            "instance."
        )
    )


class SalesforceBaseIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = SalesforceBaseIntegration
