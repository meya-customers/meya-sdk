from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.salesforce.integration import SalesforceIntegrationRef
from typing import Optional


@dataclass
class SalesforceContactMixin(Element):
    first_name: str = element_field(help="The contact's first name.")
    last_name: str = element_field(help="The contact's last name.")
    email: Optional[str] = element_field(
        default=None, help="The contact's email address."
    )
    mobile_phone: Optional[str] = element_field(
        default=None, help="The contact's mobile phone number."
    )
    phone: Optional[str] = element_field(
        default=None, help="The contact's phone number."
    )
    title: Optional[str] = element_field(
        default=None, help="Title of the contact e.g. CEO or Vice President."
    )
    custom_fields: Optional[dict] = element_field(
        default=None,
        help=(
            "Dictionary of name, value pairs used to set custom fields "
            "for the contact object. Custom fields must be defined by your "
            "Salesforce administrator. Field names must be entered using the "
            "API Name (ex. HireDate__c)."
        ),
    )
    integration: SalesforceIntegrationRef = element_field()
