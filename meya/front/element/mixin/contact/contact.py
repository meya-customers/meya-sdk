from dataclasses import dataclass
from meya.element.field import element_field
from meya.front.element.mixin.contact.base import FrontContactBase
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class FrontContactMixin(FrontContactBase):
    name: Optional[str] = element_field(
        default=None, name="The contact's name"
    )
    description: Optional[str] = element_field(
        default=None, help="A description of the contact"
    )
    avatar_url: Optional[str] = element_field(
        default=None, help="The URL of an image to use as the contact's avatar"
    )
    group_names: Optional[List[str]] = element_field(
        default=None,
        help=(
            "List of all the group names the contact belongs to. "
            "Missing groups will be created automatically."
        ),
    )
    is_spammer: Optional[bool] = element_field(
        default=None,
        help="Indicates whether or not the contact is marked as a spammer",
    )
    links: Optional[List[str]] = element_field(
        default=None, help="A list of all the links of the contact"
    )

    custom_fields: Optional[Dict[str, Any]] = element_field(
        default_factory=dict,
        help=(
            "Custom field attributes for this contact. Leave empty if "
            "you do not wish to update the attributes. Not sending existing "
            "attributes will automatically remove them."
        ),
    )
