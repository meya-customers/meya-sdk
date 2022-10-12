from dataclasses import dataclass
from meya.button.trigger import ButtonTrigger
from meya.element.field import process_field
from meya.widget.event.page.button_click import PageButtonClickEvent


@dataclass
class PageButtonTrigger(ButtonTrigger):
    entry: PageButtonClickEvent = process_field()
    encrypted_entry: PageButtonClickEvent = process_field()
