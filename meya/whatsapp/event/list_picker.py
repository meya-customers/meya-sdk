from dataclasses import dataclass
from meya.button.spec import ButtonEventSpec
from meya.entry.field import entry_field
from meya.event.entry import Event
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.whatsapp.component.spec import ListPickerItemElementSpec
from typing import List
from typing import Optional


@dataclass
class ListPickerItemEventSpec(ButtonEventSpec):
    description: Optional[str] = None

    @classmethod
    def from_element_spec_union_list(
        cls,
        items: List[ListPickerItemElementSpec],
        skip_triggers: bool = False,
    ) -> (List["ListPickerItemEventSpec"], List[TriggerActivateEntry]):
        triggers = []
        item_results = []
        for item in items:
            new_button_result, new_triggers = cls.from_element_spec_union(
                item, skip_triggers=skip_triggers
            )
            new_item_result = ListPickerItemEventSpec(
                url=new_button_result.url,
                javascript=new_button_result.javascript,
                button_id=new_button_result.button_id,
                context=new_button_result.context,
                disabled=new_button_result.disabled,
                divider=new_button_result.divider,
                icon=new_button_result.icon,
                menu=new_button_result.menu,
                text=new_button_result.text,
                description=item.description,
            )
            item_results += [new_item_result] if new_item_result else []
            triggers += new_triggers
        return item_results, triggers


@dataclass
class ListPickerEvent(Event):
    body: Optional[str] = entry_field(default=None, sensitive=True)
    button: Optional[str] = entry_field(default=None, sensitive=True)
    items: List[ListPickerItemEventSpec] = entry_field(sensitive_factory=list)

    def to_transcript_text(self) -> str:
        return "\n".join(
            [
                self.body or "...",
                *[item.to_transcript_text() for item in self.items],
            ]
        )
