from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.integration.element import Integration
from meya.salesforce.integration.base import SalesforceBaseIntegration
from meya.salesforce.integration.base import SalesforceBaseIntegrationRef
from typing import ClassVar
from typing import Optional
from typing import Type


@dataclass
class SalesforceKnowledgeIntegration(Integration, SalesforceBaseIntegration):
    """
    # Install instructions

    ### Salesforce Access Token documentation:
    - `https://developer.salesforce.com/docs/atlas.en-us.api_iot.meta/api_iot/qs_auth_access_token.htm`

    ### Salesforce user
    - Create or select a Salesforce user to be used as the integration user.
    - Get the user's username used to login to Salesforce (e.g. bot@meya.ai).
    - Get the user's password used to login on Salesforce.
    - Past the `username` and `password` into the vault variables.

    ### Create app
    - From Salesforce classic, go to Setup > Build > Create > Apps > Connected App (section) > New.
    - Grant the necessary permissions.

    ### Get Api credentials
    - On the recently created app go to `API (Enable OAuth Settings)` section.
    - Copy the `Consumer Key` and `Consumer Secret` and paste to `client_id` and `client_secret` vault variables, respectively.

    ### Knowledge site base URL
    - Get the site base URL at Classic > Setup > Build > Develop > Sites
    """

    NAME: ClassVar[str] = "salesforce_knowledge"
    knowledge_base_url: Optional[str] = element_field(
        default=None,
        help=(
            "The Salesforce Knowledge site base URL. "
            "You can get the site URL at "
            "Classic > Setup > Build > Develop > Sites. "
            "This is used for building the article URL in the "
            "`meya.salesforce.knowledge.component.display` component."
        ),
    )


class SalesforceKnowledgeIntegrationRef(SalesforceBaseIntegrationRef):
    element_type: ClassVar[Type[Element]] = SalesforceKnowledgeIntegration
