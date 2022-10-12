from dataclasses import dataclass
from meya.button.trigger import ButtonTrigger
from meya.element.field import process_field
from meya.widget.event.field.button_click import FieldButtonClickEvent


@dataclass
class FieldButtonTrigger(ButtonTrigger):
    entry: FieldButtonClickEvent = process_field()
    encrypted_entry: FieldButtonClickEvent = process_field()
