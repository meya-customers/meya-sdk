from dataclasses import dataclass
from meya.element.field import element_field
from meya.integration.element import Integration


@dataclass
class ZendeskBaseIntegration(Integration):
    subdomain: str = element_field(
        help=(
            "The subdomain of your Zendesk instance. You'll find this "
            "in the actual URL of your Zendesk instance e.g. "
            "https://subdomain.zendesk.com/"
        )
    )
    bot_agent_email: str = element_field(
        help=(
            "The email address of the Zendesk user you created to "
            "represent the bot agent. All API calls the integration makes "
            "will use this user's Zendesk API token."
        )
    )
    bot_agent_api_token: str = element_field(
        help=(
            "The API token of the user you created to represent the bot agent."
        )
    )
