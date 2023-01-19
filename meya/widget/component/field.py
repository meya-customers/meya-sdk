from dataclasses import MISSING
from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerActionEntry
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from meya.util.generate_id import generate_button_id
from meya.util.generate_id import generate_field_id
from meya.widget.component.component import WidgetComponent
from meya.widget.component.component import WidgetMode
from meya.widget.event.field import FieldEvent
from meya.widget.event.field.button_click import FieldButtonClickEvent
from meya.widget.trigger.field.button_trigger import FieldButtonTrigger
from typing import List
from typing import Optional
from typing import Tuple


class FieldAction(SimpleEnum):
    SUBMIT = "submit"


@dataclass
class FieldComponent(WidgetComponent):
    """
    A field component is a component that can be displayed both as a chat
    input, or as form field in a page. This is the base field component that
    is used by **all** other field components.

    This is an **abstract** component and should **not** be used directly in
    your BFML.

    Check the [Widgets & Pages](https://docs.meya.ai/docs/widgets-and-pages) guide for more info on creating advanced
    form wizards for collecting user input using field components.
    """

    @dataclass
    class Next:
        field_action: FieldAction = response_field()

    is_abstract: bool = meta_field(value=True)

    required: bool = element_field(default=False)
    label: Optional[str] = element_field(default=None)
    disabled: bool = element_field(default=False)

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        super().post_process(entry, extra_entries)

        if isinstance(entry, FieldEvent):
            if entry.field_id is MISSING:
                entry.field_id = self.get_field_id()

            if entry.submit_button_id is MISSING:
                (
                    submit_trigger,
                    submit_button_id,
                ) = self.get_field_action_button_id_and_trigger(
                    FieldAction.SUBMIT
                )
                entry.submit_button_id = submit_button_id
                if submit_trigger:
                    extra_entries.append(submit_trigger)

            if entry.required is MISSING:
                entry.required = self.required

            if entry.label is MISSING:
                entry.label = self.label

            if entry.disabled is MISSING:
                entry.disabled = self.disabled

            if entry.ok is MISSING:
                entry.ok = (
                    self.input_validation.ok
                    if self.mode == WidgetMode.STANDALONE
                    else None
                )

            if entry.error is MISSING:
                entry.error = self.input_validation.error

            if entry.input_data is MISSING:
                entry.input_data = (
                    self.input_data
                    if self.mode == WidgetMode.STANDALONE
                    else None
                )

    @property
    def skip_triggers(self) -> bool:
        return self.mode != WidgetMode.STANDALONE or self.input_validation.ok

    async def next(self) -> List[Entry]:
        encrypted_event: FieldButtonClickEvent = (
            FieldButtonClickEvent.from_typed_dict(
                self.entry.data[Trigger.EVENT_KEY]
            )
        )
        event = await self.db.try_decrypt_sensitive_entry(encrypted_event)
        field_action = from_dict(self.Next, self.entry.data).field_action
        if field_action == FieldAction.SUBMIT:
            entries = await self.get_build_result(
                WidgetMode.STANDALONE, event.input_data
            )
            return self.respond(
                *entries,
                data=self.Response(result=self.input_validation.validated_data)
                if self.input_validation.ok
                else None,
            )
        else:
            raise NotImplementedError()

    def get_field_id(self) -> Optional[str]:
        if self.mode != WidgetMode.STANDALONE:
            return None
        if self.next_entry:
            encrypted_event: FieldButtonClickEvent = (
                FieldButtonClickEvent.from_typed_dict(
                    self.entry.data[Trigger.EVENT_KEY]
                )
            )
            return encrypted_event.field_id
        else:
            return generate_field_id()

    def get_field_action_button_id_and_trigger(
        self, field_action: FieldAction
    ) -> Tuple[Optional[TriggerActivateEntry], Optional[str]]:
        if self.skip_triggers:
            return None, None
        [action_entry] = self.flow_control_component_next(
            data=to_dict(self.Next(field_action=field_action))
        )
        button_id = generate_button_id()
        trigger = FieldButtonTrigger(
            button_id=button_id,
            action=TriggerActionEntry(action_entry.to_typed_dict()),
            text=to_dict(field_action),
        )
        return trigger.activate(), button_id
