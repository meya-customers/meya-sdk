from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.text.trigger import TextTrigger
from meya.util.enum import SimpleEnum
from meya.zendesk.help_center.element.mixin import ZendeskHelpCenterMixin
from typing import Optional


@dataclass
class ZendeskHelpCenterTriggerResponse:
    search_query: str = response_field(sensitive=True)
    zendesk_help_desk_response: dict = response_field(sensitive=True)


class Expect(SimpleEnum):
    ZendeskHelpCenter = "zendesk_help_center"


@dataclass
class ZendeskHelpCenterTrigger(TextTrigger, ZendeskHelpCenterMixin):
    expect: Optional[Expect] = element_field(signature=True, default=None)
    query: Optional[str] = element_field(
        default=None,
        help=(
            "The search text to be matched or a search string. "
            'Examples: "bluetooth help", "\'bluetooth help\'".'
        ),
    )
