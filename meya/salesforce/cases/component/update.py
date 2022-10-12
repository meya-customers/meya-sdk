from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.cases.element.mixin import SalesforceCaseMixin
from meya.salesforce.cases.payload import SalesforceCasesUpdateResponse
from typing import Optional


@dataclass
class SalesforceCasesUpdateComponentResponse(ApiComponentResponse):
    result: SalesforceCasesUpdateResponse = response_field(sensitive=True)


@dataclass
class SalesforceCasesUpdateComponent(BaseApiComponent, SalesforceCaseMixin):
    case_id: Optional[str] = element_field(
        default=None,
        help=(
            "The unique identifier of the case you would like to update."
            "This appears as `id` on Api responses."
        ),
    )
