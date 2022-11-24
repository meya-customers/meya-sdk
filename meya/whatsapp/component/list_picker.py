from dataclasses import dataclass
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from meya.user.meta_tag import UserInputTag
from meya.whatsapp.component.spec import ListPickerItemElementSpec
from meya.whatsapp.event.list_picker import ListPickerEvent
from meya.whatsapp.event.list_picker import ListPickerItemEventSpec
from typing import List
from typing import Optional
from typing import Type


@dataclass
class ListPickerComponent(Component):
    """
    Show a WhatsApp list picker containing a list of buttons for the user to
    select.
    """

    meta_name: str = meta_field(value="List Picker")
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/01-interface-essential/48-select/cursor.svg"
    )
    meta_level: float = meta_field(value=MetaLevel.VERY_BASIC_TOP)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[UserInputTag])
    snippet_default: str = meta_field(
        value="""
            list_picker: How can I help?
            button: Select an option
            items:
              - text: Yes
                description: Select Yes to continue
                action: next
              - text: No
                description: Select No to stop
                action: next
        """
    )

    list_picker: Optional[str] = element_field(
        signature=True, default=None, help="The list picker body text"
    )
    items: List[ListPickerItemElementSpec] = element_field(
        help="List of buttons that the user can select"
    )
    button: Optional[str] = element_field(default=None)

    async def start(self) -> List[Entry]:
        items, triggers = ListPickerItemEventSpec.from_element_spec_union_list(
            self.items, skip_triggers=self.skip_triggers
        )
        event = ListPickerEvent(
            body=self.list_picker,
            button=self.button,
            items=items,
        )
        return self.respond(event, *triggers)
