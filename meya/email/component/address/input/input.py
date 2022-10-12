from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.email.trigger.address import EmailAddressTrigger
from meya.text.component.input.base import BaseTextInputComponent
from meya.text.event.input import TextInputType
from meya.widget.component.component import WidgetInputValidationError
from typing import Any
from typing import ClassVar


@dataclass
class EmailAddressInputComponent(BaseTextInputComponent):
    extra_alias: str = meta_field(value="email_address_input")
    error_message: str = element_field(
        default="Please enter a valid email address.",
        level=MetaLevel.INTERMEDIATE,
    )

    input_type: ClassVar[TextInputType] = TextInputType.EMAIL

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, str)
        if not self.input_data and not self.required:
            return self.input_data
        result = EmailAddressTrigger.validate_email(self.input_data)
        if not result:
            raise WidgetInputValidationError(self.error_message)
        return result
