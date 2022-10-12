from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse as date_parse
from meya.element import Element
from meya.element.field import element_field
from meya.salesforce.cases.integration import SalesforceCasesIntegrationRef
from typing import Optional
from typing import Union


@dataclass
class SalesforceCaseMixin(Element):
    description: Optional[str] = element_field(
        default=None, help="A text description of the case."
    )
    comments: Optional[str] = element_field(
        default=None,
        help=(
            "Used to insert a new CaseComment. Note: This is a single comment "
            "string, not a list of strings due to a misnomer in Salesforce API"
        ),
    )
    contact_id: Optional[str] = element_field(
        default=None, help="ID of the associated contact."
    )
    is_escalated: Optional[bool] = element_field(
        default=None,
        help=(
            "Indicates whether the case has been escalated (true) or not. "
            "A case's escalated state does not affect how you can use a case, "
            "or whether you can query, delete, or update it."
        ),
    )
    origin: Optional[str] = element_field(
        default=None,
        help="The source of the case, such as Email, Phone, or Web.",
    )
    owner_id: Optional[str] = element_field(
        default=None, help="ID of the contact who owns the case."
    )
    parent_id: Optional[str] = element_field(
        default=None, help="The ID of the parent case in the hierarchy"
    )
    priority: Optional[str] = element_field(
        default=None,
        help=(
            "The importance or urgency of the case, such as "
            "High, Medium, or Low."
        ),
    )
    reason: Optional[str] = element_field(
        default=None,
        help=(
            "The reason why the case was created, "
            "such as 'Instructions not clear' or 'User didn't attend training'."
        ),
    )
    source_id: Optional[str] = element_field(
        default=None, help="The ID of the social post source."
    )
    status: Optional[str] = element_field(
        default=None,
        help=(
            "The status of the case, such as New, Closed, or Escalated. "
            "This field directly controls the IsClosed flag."
        ),
    )
    subject: Optional[str] = element_field(
        default=None, help="The subject of the case."
    )
    supplied_company: Optional[str] = element_field(
        default=None,
        help="The company name that was entered when the case was created.",
    )
    supplied_email: Optional[str] = element_field(
        default=None,
        help="The email address that was entered when the case was created.",
    )
    supplied_name: Optional[str] = element_field(
        default=None,
        help="The name that was entered when the case was created.",
    )
    supplied_phone: Optional[str] = element_field(
        default=None,
        help="The phone number that was entered when the case was created.",
    )
    case_type: Optional[str] = element_field(
        default=None,
        help="The type of case, such as Feature Request or Question.",
    )
    last_referenced_date: Optional[Union[str, datetime]] = element_field(
        default=None,
        help=(
            "The timestamp when the current user last accessed this record, "
            "a record related to this record, or a list view."
            "Accepted formats: YYYY-MM-DD, YYYY-MM-DDThh:mm:ss+hh:mm, YYYY-MM-DDThh:mm:ss-hh:mm or "
            "YYYY-MM-DDThh:mm:ssZ. "
            "Ready-only field you'll need special permission to edit this field."
        ),
    )
    last_viewed_date: Optional[Union[str, datetime]] = element_field(
        default=None,
        help=(
            "The timestamp when the current user last viewed this record or "
            "list view. "
            "If this value is null, the user might have only accessed this "
            "record or list view (LastReferencedDate) but not viewed it."
            "Accepted formats: YYYY-MM-DD, YYYY-MM-DDThh:mm:ss+hh:mm, YYYY-MM-DDThh:mm:ss-hh:mm or "
            "YYYY-MM-DDThh:mm:ssZ. "
            "Ready-only field you'll need special permission to edit this field."
        ),
    )
    master_record_id: Optional[str] = element_field(
        default=None,
        help=(
            "If this object was deleted as the result of a merge, "
            "this field contains the ID of the record that was kept. "
            "If this object was deleted for any other reason, "
            "or has not been deleted, the value is null."
            "Ready-only field you'll need special permission to change this field."
        ),
    )
    contact_mobile: Optional[str] = element_field(
        default=None,
        help=(
            "Mobile telephone number for the contact. "
            "Ready-only field you'll need special permission to change this field."
        ),
    )
    contact_phone: Optional[str] = element_field(
        default=None,
        help=(
            "Telephone number for the contact. "
            "Ready-only field you'll need special permission to change this field."
        ),
    )
    closed_date: Optional[Union[str, datetime]] = element_field(
        default=None,
        help=(
            "The date and time when the case was closed."
            "Accepted formats: YYYY-MM-DD, YYYY-MM-DDThh:mm:ss+hh:mm, YYYY-MM-DDThh:mm:ss-hh:mm or "
            "YYYY-MM-DDThh:mm:ssZ. "
            "Ready-only field you'll need special permission to edit this field."
        ),
    )
    contact_email: Optional[str] = element_field(
        default=None,
        help=(
            "Email address for the contact. "
            "Ready-only field you'll need special permission to edit this field."
        ),
    )
    contact_fax: Optional[str] = element_field(
        default=None,
        help=(
            "Fax number for the contact. "
            "Ready-only field you'll need special permission to change this field"
        ),
    )
    is_deleted: Optional[bool] = element_field(
        default=None,
        help=(
            "Indicates whether the object has been moved to the "
            "Recycle Bin (true) or not (false)."
            "Ready-only field you'll need special permission to change this field."
        ),
    )
    custom_fields: Optional[dict] = element_field(
        default=None,
        help=(
            "Dictionary of name, value pairs used to set custom fields "
            "for the case object. Custom fields must be defined by your "
            "Salesforce administrator. Field names must be entered using the "
            "API Name (ex. HireDate__c)."
        ),
    )
    integration: SalesforceCasesIntegrationRef = element_field()

    def validate(self):
        super().validate()
        try:
            if self.closed_date and isinstance(self.closed_date, str):
                date_parse(self.closed_date)
            if self.last_viewed_date and isinstance(
                self.last_viewed_date, str
            ):
                date_parse(self.last_viewed_date)
            if self.last_referenced_date and isinstance(
                self.last_referenced_date, str
            ):
                date_parse(self.last_referenced_date)
        except ValueError:
            raise self.validation_error(
                (
                    "Invalid date format."
                    "Accepted formats: YYYY-MM-DD, YYYY-MM-DDThh:mm:ss+hh:mm, YYYY-MM-DDThh:mm:ss-hh:mm or "
                    "YYYY-MM-DDThh:mm:ssZ. "
                    "Check https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/"
                    "sforce_api_calls_soql_select_dateformats.htm for more details."
                )
            )
