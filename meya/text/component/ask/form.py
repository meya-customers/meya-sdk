from dataclasses import dataclass
from dataclasses import field
from meya.component.element import ComponentOkResponse
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from meya.util.generate_id import generate_form_id
from typing import List
from typing import Optional


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)


@dataclass
class AskFormComponent(InteractiveComponent):
    ask_form: Optional[str] = element_field(signature=True, default=None)
    icon: Optional[IconElementSpecUnion] = element_field(default=None)
    field_name: Optional[str] = element_field(default="text")
    autocomplete: Optional[str] = element_field(default="off")
    label: str = element_field(default="Text")
    placeholder: Optional[str] = element_field(default=None)
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
                    type=FieldType.TEXT,
                )
            ],
            text=self.ask_form,
        )
        return self.respond(
            ask_form_event, self.trigger(ask_form_event.form_id)
        )

    async def next(self) -> List[Entry]:
        encrypted_form_submit_event: FormSubmitEvent = Entry.from_typed_dict(
            self.entry.data["event"]
        )
        form_submit_event = await self.db.try_decrypt_sensitive_entry(
            encrypted_form_submit_event
        )
        input_result = ComponentOkResponse(
            result=form_submit_event.fields[self.field_name]
        )
        form_ok_event = FormOkEvent(form_id=form_submit_event.form_id)
        return self.respond(form_ok_event, data=input_result)

    def trigger(self, form_id: str):
        return FormTrigger(
            action=self.get_next_action(), form_id=form_id
        ).activate()
