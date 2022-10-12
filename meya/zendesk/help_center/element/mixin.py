from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.zendesk.help_center.integration import (
    ZendeskHelpCenterIntegrationRef,
)
from meya.zendesk.help_center.payload.query import ZendeskHelpCenterSortBy
from meya.zendesk.help_center.payload.query import ZendeskHelpCenterSortOrder
from typing import Optional


@dataclass
class ZendeskHelpCenterMixin(Element):
    query: str = element_field(
        help=(
            "The search text to be matched or a search string. "
            'Examples: "bluetooth help", "\'bluetooth help\'".'
        )
    )
    label_names: Optional[str] = element_field(
        default=None, help="A comma-separated list of label names."
    )
    locale: Optional[str] = element_field(
        default=None, help="Search for articles in the specified locale."
    )
    category: Optional[int] = element_field(
        default=None, help="Limit the search to this category id."
    )
    section: Optional[int] = element_field(
        default=None, help="Limit the search to this section id."
    )
    sort_by: Optional[ZendeskHelpCenterSortBy] = element_field(
        default=None,
        help=(
            "One of created_at or updated_at. Defaults to sorting by "
            "relevance."
        ),
    )
    sort_order: Optional[ZendeskHelpCenterSortOrder] = element_field(
        default=None, help="One of asc or desc. Defaults to desc."
    )
    created_after: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles created after a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    created_at: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles created on a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    created_before: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles created before a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    updated_after: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles updated after a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    updated_at: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles updated on a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    updated_before: Optional[str] = element_field(
        default=None,
        help=(
            "Limit the search to articles updated before a given date "
            "(format YYYY-MM-DD)."
        ),
    )
    page: int = element_field(
        default=1, help="Page number. Used for scroll the pagination."
    )

    per_page: int = element_field(
        default=25, help="Maximum number of articles to retrieve per request"
    )

    integration: ZendeskHelpCenterIntegrationRef = element_field()
