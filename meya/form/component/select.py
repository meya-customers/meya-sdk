from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonEventSpec
from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.form.error import FormValidationError
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.error import FormErrorEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.spec import SelectOptionElementSpecUnion
from meya.form.spec import SelectOptionEventSpec
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.util.generate_id import generate_form_id
from numbers import Real
from typing import Any
from typing import List
from typing import Optional
from typing import Union


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class SelectComponent(InteractiveComponent):
    select: str = element_field(
        signature=True,
        default="Select",
        help="Label shown to describe this field",
    )
    icon: Optional[IconElementSpecUnion] = element_field(
        default=None, help="Icon shown for this field"
    )
    name: str = element_field(
        default="select", help="Name of the input element"
    )
    autocomplete: Optional[str] = element_field(
        default="off", help="Autocomplete mode for this field"
    )
    no_results_text: str = element_field(
        default="No results",
        help="Text shown when no matches were found via search",
    )
    custom: bool = element_field(
        default=False, help="Whether custom values can be entered"
    )
    search: bool = element_field(
        default=False, help="Whether the user can type to search the options"
    )
    placeholder: Optional[str] = element_field(default=None)
    multi: bool = element_field(
        default=False, help="Whether multiple options can be selected"
    )
    default: Optional[Union[str, List[str]]] = element_field(
        default=None, help="Default selected option (text)"
    )
    options: List[SelectOptionElementSpecUnion] = element_field(
        help="Options available for selection"
    )
    retries: Real = element_field(
        default=float("inf"),
        help="Number of retries before flow continues with error",
    )
    error_message: str = element_field(
        default="Invalid value selected",
        help="Message shown if input is invalid",
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    def validate(self):
        super().validate()
        if isinstance(self.default, str):
            if self.multi:
                raise self.validation_error(
                    "default must be a list for multi-select"
                )
        elif isinstance(self.default, list):
            if not self.multi:
                raise self.validation_error(
                    "default must be a string for single-select"
                )
        elif self.multi and self.search:
            raise self.validation_error("multi-select does not support search")
        elif self.multi and self.custom:
            raise self.validation_error(
                "multi-select does not support custom values"
            )

    async def start(self) -> List[Entry]:
        ask_form_event = FormAskEvent(
            form_id=generate_form_id(), fields=[self.create_field()]
        )
        self.reset()
        return self.respond(
            ask_form_event, self.trigger(ask_form_event.form_id)
        )

    def create_field(self) -> Field:
        return Field(
            name=self.name,
            autocomplete=self.autocomplete,
            icon=IconEventSpec.from_element_spec(self.icon),
            placeholder=self.placeholder,
            label=self.select,
            no_results_text=self.no_results_text,
            required=True,
            type=FieldType.SELECT,
            custom=self.custom,
            search=self.search,
            multi=self.multi,
            options=[
                SelectOptionEventSpec(text=option)
                if isinstance(option, str)
                else SelectOptionEventSpec(
                    text=option.text, disabled=option.disabled
                )
                for option in self.options
            ],
            default=self.default,
        )

    async def next(self) -> List[Entry]:
        # TODO Validate all form fields and extract this field instead
        #      of just validating and extracting this field
        encrypted_form_submit_event: FormSubmitEvent = Entry.from_typed_dict(
            self.entry.data["event"]
        )
        form_submit_event = await self.db.try_decrypt_sensitive_entry(
            encrypted_form_submit_event
        )
        original_result = form_submit_event.fields[self.name]

        try:
            result = self.validate_result(original_result)
        except FormValidationError:
            input_result = ComponentErrorResponse(
                result=original_result,
                retry_count=self.entry.data.get(self.RETRY_COUNT_KEY, 0),
            )
            if input_result.retry_count == self.retries:
                return self.respond(data=input_result)
            else:
                input_result.retry_count += 1
                (
                    quick_replies,
                    quick_reply_triggers,
                ) = ButtonEventSpec.from_element_spec_union_list(
                    self.quick_replies
                )
                form_error_event = FormErrorEvent(
                    composer=ComposerEventSpec(
                        focus=None,
                        placeholder=self.composer.placeholder,
                        visibility=self.composer.visibility,
                    ),
                    form_id=form_submit_event.form_id,
                    fields={self.name: self.error_message},
                    quick_replies=quick_replies,
                )
                return [
                    form_error_event,
                    self.trigger(form_submit_event.form_id, data=input_result),
                    *quick_reply_triggers,
                ]
        else:
            input_result = ComponentOkResponse(result=result)
            form_ok_event = FormOkEvent(form_id=form_submit_event.form_id)
            return self.respond(form_ok_event, data=input_result)

    def validate_result(self, original_result: Any) -> Any:
        if self.multi:
            if (
                not isinstance(original_result, list)
                or len(original_result) == 0
            ):
                raise FormValidationError()
            else:
                return [
                    self.validate_single_result(original_result_item)
                    for original_result_item in original_result
                ]
        else:
            return self.validate_single_result(original_result)

    def validate_single_result(self, original_result: Any) -> Any:
        if not isinstance(original_result, str):
            raise FormValidationError

        matched_option = next(
            (
                option
                for option in self.options
                if (
                    original_result == option
                    if isinstance(option, str)
                    else original_result == option.text
                )
            ),
            None,
        )
        if matched_option is None:
            if not self.custom:
                raise FormValidationError()
            else:
                return original_result
        if not isinstance(matched_option, str) and matched_option.disabled:
            raise FormValidationError()

        if isinstance(matched_option, str) or matched_option.value is MISSING:
            return original_result
        else:
            return matched_option.value

    def trigger(self, form_id: str, *, data: Any = None):
        return FormTrigger(
            action=self.get_next_action(data=data), form_id=form_id
        ).activate()
