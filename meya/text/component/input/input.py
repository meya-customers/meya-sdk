from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.text.component.input.base import BaseTextInputComponent
from meya.widget.component.component import WidgetInputValidationError
from typing import Any


@dataclass
class TextInputComponent(BaseTextInputComponent):
    extra_alias: str = meta_field(value="text_input")
    error_message: str = element_field(
        default="Please enter a value.", level=MetaLevel.INTERMEDIATE
    )

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, str)
        if not self.input_data and self.required:
            raise WidgetInputValidationError(self.error_message)
        return self.input_data
