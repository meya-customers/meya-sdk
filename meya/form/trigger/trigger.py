from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import process_field
from meya.form.event.submit import FormSubmitEvent
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerMatchResult
from meya.trigger.element import TriggerResponse


@dataclass
class FormTrigger(Trigger):
    form_id: str = element_field()

    entry: FormSubmitEvent = process_field()
    encrypted_entry: FormSubmitEvent = process_field()

    async def match(self) -> TriggerMatchResult:
        if self.form_id == self.entry.form_id:
            return self.succeed(
                data=TriggerResponse(result=self.encrypted_entry.fields)
            )
        else:
            return self.fail()
