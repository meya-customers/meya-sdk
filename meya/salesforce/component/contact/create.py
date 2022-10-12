from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.element.mixin import SalesforceContactMixin
from meya.salesforce.payload.contact import SalesforceCreateContactResponse
from typing import Optional


@dataclass
class SalesforceContactCreateResponse(ApiComponentResponse):
    result: SalesforceCreateContactResponse = response_field(sensitive=True)


@dataclass
class SalesforceContactCreateComponent(
    BaseApiComponent, SalesforceContactMixin
):
    link: Optional[bool] = element_field(
        default=False,
        help=(
            "Links the current Meya user with the integration user when "
            "`true` (coming soon)."
        ),
    )

    def validate(self):
        super().validate()
        if self.link:
            raise self.validation_error(
                "Linking is not supported yet (coming soon)."
            )
