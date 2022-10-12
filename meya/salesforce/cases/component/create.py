from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.cases.element.mixin import SalesforceCaseMixin
from meya.salesforce.cases.payload import SalesforceCasesCreateResponse
from typing import Optional


@dataclass
class SalesforceCasesCreateComponentResponse(ApiComponentResponse):
    result: SalesforceCasesCreateResponse = response_field(sensitive=True)


@dataclass
class SalesforceCasesCreateComponent(BaseApiComponent, SalesforceCaseMixin):
    send_transcript: bool = element_field(
        default=False,
        help="Send the conversation transcript as a case comment to the case.",
    )
    account_id: Optional[str] = element_field(
        default=None, help="The ID of the account associated with this case."
    )
    contact_first_name: Optional[str] = element_field(
        default=None,
        help=(
            "The contact's first name. If not provided the contact's first "
            "name will be `Meya User`."
        ),
    )
    contact_last_name: Optional[str] = element_field(
        default=None,
        help=(
            "The contact's last name. If not provided the contact's last "
            "name will be `id: MEYA_USER_ID`."
        ),
    )
    link: Optional[bool] = element_field(
        default=False,
        help=(
            "Links the current thread with the integration thread when `true`."
            "This allows `salesforce.case.component.update` "
            "and `salesforce.case.component.add_comment` components to be "
            "used without the `case_id` parameter, also, this parameter will "
            "control whether new messages sent by user using orb should "
            "be relayed to the case (coming soon)."
        ),
    )

    def validate(self):
        super().validate()
        if self.link:
            raise self.validation_error(
                "Linking is not supported yet (coming soon)."
            )
