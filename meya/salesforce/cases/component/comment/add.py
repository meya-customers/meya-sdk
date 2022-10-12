from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.cases.integration import SalesforceCasesIntegrationRef
from meya.salesforce.cases.payload import SalesforceCasesAddCommentResponse
from typing import Optional


@dataclass
class SalesforceCasesAddCommentComponentResponse(ApiComponentResponse):
    result: SalesforceCasesAddCommentResponse = response_field(sensitive=True)


@dataclass
class SalesforceCasesAddCommentComponent(BaseApiComponent):
    comment: str = element_field(help="The comment text to add to a case.")
    case_id: Optional[str] = element_field(
        default=None,
        help=(
            "The unique identifier of the case you would like to update."
            "This appears as `id` on Api responses."
        ),
    )
    integration: SalesforceCasesIntegrationRef = element_field()
