from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import response_field
from meya.text.component.input.base import BaseTextInputComponent
from meya.text.ignorecase import IgnorecaseMixin
from meya.text.trigger.regex import RegexTrigger
from meya.widget.component.component import WidgetInputValidationError
from typing import Any
from typing import Optional
from typing import Union


@dataclass
class RegexInputComponent(BaseTextInputComponent, IgnorecaseMixin):
    @dataclass
    class Response(BaseTextInputComponent.Response):
        result: Union[str, dict] = response_field(sensitive=True)

    regex_input: str = element_field(signature=True)
    capture_groups: bool = element_field(default=False)
    ignorecase: Optional[bool] = element_field(default=None)
    error_message: str = element_field(
        default="Invalid input, please try again.",
        level=MetaLevel.INTERMEDIATE,
    )

    async def validate_input_data(self) -> Any:
        assert isinstance(self.input_data, str)
        match = RegexTrigger.search_regex(
            self.regex_input, self.input_data, self.ignorecase_default_true
        )
        if not match:
            raise WidgetInputValidationError(self.error_message)
        match_result, match_groups = match
        if not self.capture_groups:
            return match_result
        else:
            return match_groups
