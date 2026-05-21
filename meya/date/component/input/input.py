from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from meya.core.meta_level import MetaLevel
from meya.date.event.input import DateInputEvent
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.widget.component.component import WidgetInputValidationError
from meya.widget.component.field import FieldComponent
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class DateInputComponent(FieldComponent):
    """
    Get a date input from the user using a native date picker. This component
    renders an `<input type="date">` in the Orb Web SDK, providing a
    browser-native calendar picker.

    ```yaml
    - type: meya.date.component.input
      label: Date of birth
      required: true
    ```

    The date input component is also an interactive component which allows you
    to set [quick replies](https://docs.meya.ai/docs/buttons-and-quick-replies),
    configure the [input composer](https://docs.meya.ai/docs/composer)
    and set context data.

    ### Configuration

    - `min` / `max`: Restrict selectable dates (ISO format `YYYY-MM-DD`).
    - `default`: Pre-populate with an ISO date string.

    ### Input validation

    If `required` is `true`, an error is shown when the user submits without
    selecting a date. Dates outside the `min`/`max` range are also rejected.

    The selected date is stored in `(@ flow.result )` as an ISO format
    string (`YYYY-MM-DD`).

    ### Pages support
    This date input component is also a widget component that can be displayed
    as a field in a page.

    ```yaml
    - page:
      - type: meya.date.component.input
        label: Appointment date
        required: true
    ```

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages)
    guide for more info on creating advanced form wizards for collecting user
    input.
    """

    extra_alias: str = meta_field(value="date_input")

    @dataclass
    class Response(FieldComponent.Response):
        result: str = response_field(sensitive=True)

    icon: Optional[IconElementSpecUnion] = element_field(
        default=None,
        help=(
            "The icon spec or URL to use for the input field. See the "
            "[Icons](https://docs.meya.ai/docs/icons) guide for more info."
        ),
    )
    default: Optional[str] = element_field(
        default=None,
        help="The input's default value in ISO format (YYYY-MM-DD).",
    )
    min: Optional[str] = element_field(
        default=None,
        help="The earliest selectable date in ISO format (YYYY-MM-DD).",
    )
    max: Optional[str] = element_field(
        default=None,
        help="The latest selectable date in ISO format (YYYY-MM-DD).",
    )
    error_message: str = element_field(
        default="Please select a valid date.",
        level=MetaLevel.INTERMEDIATE,
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec,
        level=MetaLevel.ADVANCED,
        help=(
            "The composer spec that allows you to control the Orb's input "
            "composer. Check the "
            "[Composer](https://docs.meya.ai/docs/composer) guide for more "
            "info."
        ),
    )

    async def build(self) -> List[Entry]:
        event = DateInputEvent(
            default=self.default,
            icon=IconEventSpec.from_element_spec(self.icon),
            min=self.min,
            max=self.max,
        )
        return self.respond(event)

    async def validate_input_data(self):
        assert isinstance(self.input_data, str)
        if not self.input_data:
            if self.required:
                raise WidgetInputValidationError(self.error_message)
            return self.input_data

        try:
            date = datetime.strptime(self.input_data, "%Y-%m-%d")
        except ValueError:
            raise WidgetInputValidationError(self.error_message)

        if self.min:
            try:
                min_date = datetime.strptime(self.min, "%Y-%m-%d")
            except ValueError as e:
                raise ValueError(
                    f"DateInputComponent: invalid `min` {self.min!r}, "
                    f"expected YYYY-MM-DD"
                ) from e
            if date < min_date:
                raise WidgetInputValidationError(self.error_message)

        if self.max:
            try:
                max_date = datetime.strptime(self.max, "%Y-%m-%d")
            except ValueError as e:
                raise ValueError(
                    f"DateInputComponent: invalid `max` {self.max!r}, "
                    f"expected YYYY-MM-DD"
                ) from e
            if date > max_date:
                raise WidgetInputValidationError(self.error_message)

        return self.input_data
