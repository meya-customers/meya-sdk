from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonEventSpec
from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.email.trigger.address import EmailAddressTrigger
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.error import FormErrorEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.util.enum import SimpleEnum
from meya.util.generate_id import generate_form_id
from numbers import Real
from typing import Any
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


class Expect(SimpleEnum):
    EMAIL_ADDRESS = "email_address"


@dataclass
class EmailAddressAskFormComponent(InteractiveComponent):
    ask_form: Optional[str] = element_field(signature=True, default=None)
    expect: Optional[Expect] = element_field(signature=True, default=None)
    field_name: str = element_field(default="email")
    autocomplete: Optional[str] = element_field(default="email")
    label: str = element_field(default="Email")
    placeholder: Optional[str] = element_field(default="Your email address")
    icon: Optional[IconElementSpecUnion] = element_field(default=None)
    retries: Real = element_field(default=float("inf"))
    error_message: str = element_field(default="Invalid email")
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )

    async def start(self) -> List[Entry]:
        ask_form_event = FormAskEvent(
            form_id=generate_form_id(),
            fields=[
                Field(
                    name=self.field_name,
                    autocomplete=self.autocomplete,
                    icon=IconEventSpec.from_element_spec(self.icon),
                    placeholder=self.placeholder,
                    label=self.label,
                    required=True,
                    type=FieldType.EMAIL,
                )
            ],
            text=self.ask_form,
        )
        self.reset()
        return self.respond(
            ask_form_event, self.trigger(ask_form_event.form_id)
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
        original_result = form_submit_event.fields[self.field_name]

        result = EmailAddressTrigger.validate_email(original_result)
        if not result:
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
                    fields={self.field_name: self.error_message},
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

    def trigger(self, form_id: str, *, data: Any = None):
        return FormTrigger(
            action=self.get_next_action(data=data), form_id=form_id
        ).activate()
