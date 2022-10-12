import asyncio

from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event import composer_spec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerActionEntry
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from meya.util.enum import SimpleEnum
from meya.util.generate_id import generate_button_id
from meya.util.generate_id import generate_page_id
from meya.widget.component import WidgetComponent
from meya.widget.component import WidgetComponentSpec
from meya.widget.component.component import WidgetInputValidationResult
from meya.widget.component.component import WidgetMode
from meya.widget.event.page import PageEvent
from meya.widget.event.page.button_click import PageButtonClickEvent
from meya.widget.trigger.page.button_trigger import PageButtonTrigger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


class PageAction(SimpleEnum):
    SUBMIT = "submit"


@dataclass
class PageInputValidationResult:
    validated_data: Any
    ok: bool


@dataclass
class ComposerElementSpec(composer_spec.ComposerElementSpec):
    focus: Optional[ComposerFocus] = field(default=ComposerFocus.BLUR)
    visibility: Optional[ComposerVisibility] = field(
        default=ComposerVisibility.HIDE
    )


@dataclass
class PageSubmitButtonElementSpec:
    text: str = "Submit"


@dataclass
class PageComponent(InteractiveComponent):
    @dataclass
    class Next:
        page_action: PageAction = response_field()

    @dataclass
    class Response:
        result: List[Any] = response_field(sensitive=True)

    page: List[WidgetComponentSpec] = element_field(signature=True)
    submit: Optional[PageSubmitButtonElementSpec] = element_field(
        default_factory=PageSubmitButtonElementSpec
    )
    extra_buttons: List[ButtonElementSpecUnion] = element_field(
        default_factory=list,
        help="List of extra buttons used for page control",
    )
    composer: ComposerElementSpec = element_field(
        default_factory=ComposerElementSpec, level=MetaLevel.ADVANCED
    )
    input_data: Any = process_field()
    input_validation: PageInputValidationResult = process_field()

    def __post_init__(self):
        super().__post_init__()
        self.input_data = MISSING
        self.input_validation = MISSING

    @property
    def skip_triggers(self) -> bool:
        return self.input_validation.ok

    async def start(self) -> List[Entry]:
        entries = await self.get_build_result(page_id=None, input_data=None)
        return self.respond(*entries)

    async def next(self) -> List[Entry]:
        encrypted_event: PageButtonClickEvent = (
            PageButtonClickEvent.from_typed_dict(
                self.entry.data[Trigger.EVENT_KEY]
            )
        )
        event = await self.db.try_decrypt_sensitive_entry(encrypted_event)
        page_action = from_dict(self.Next, self.entry.data).page_action
        if page_action == PageAction.SUBMIT:
            entries = await self.get_build_result(
                page_id=event.page_id, input_data=event.input_data
            )
            return self.respond(
                *entries,
                data=self.Response(result=self.input_validation.validated_data)
                if self.input_validation.ok
                else None,
            )
        else:
            raise NotImplementedError()

    async def get_build_result(
        self, *, page_id: Optional[str], input_data: Optional[List[Any]]
    ) -> List[Entry]:
        self.input_data = input_data

        widget_results: Tuple[
            Tuple[List[Entry], WidgetInputValidationResult], ...
        ] = await asyncio.gather(
            *(
                self.build_widget(
                    spec,
                    self.input_data[i]
                    if self.input_data is not None
                    else None,
                )
                for i, spec in enumerate(self.page)
            )
        )
        widgets: List[Dict[str, Any]] = []
        entries: List[Entry] = []
        validated_data: List[Any] = []
        error = False
        for i, widget_result in enumerate(widget_results):
            widget_entries, widget_input_validation = widget_result
            widgets.append(widget_entries[0].to_typed_dict())
            entries += widget_entries[1:]
            if widget_input_validation.error:
                error = True
            elif widget_input_validation.ok:
                validated_data.append(widget_input_validation.validated_data)
        if self.input_data is None:
            self.input_validation = PageInputValidationResult(
                validated_data=None, ok=False
            )
        else:
            self.input_validation = PageInputValidationResult(
                validated_data=None if error else validated_data, ok=not error
            )
        page_id = page_id or generate_page_id()
        if self.submit:
            (
                submit_trigger,
                submit_button_id,
            ) = self.get_page_action_button_id_and_trigger(PageAction.SUBMIT)
            if submit_trigger:
                entries.append(submit_trigger)
        else:
            submit_button_id = None
        (
            extra_buttons,
            extra_button_triggers,
        ) = ButtonEventSpec.from_element_spec_union_list(
            self.extra_buttons, skip_triggers=self.skip_triggers
        )
        entries += extra_button_triggers
        event = PageEvent(
            page_id=page_id,
            widgets=widgets,
            input_data=self.input_data,
            submit_button_id=submit_button_id,
            submit_button_text=self.submit.text if self.submit else None,
            extra_buttons=extra_buttons,
            ok=self.input_validation.ok,
        )
        return [event, *entries]

    async def build_widget(
        self, spec: WidgetComponentSpec, widget_input_data: Any
    ) -> Tuple[List[Entry], WidgetInputValidationResult]:
        component: WidgetComponent = await self.render_from_spec(spec)
        entries = await component.get_build_result(
            WidgetMode.PAGE, widget_input_data, post_process=True
        )
        return entries, component.input_validation

    def get_page_action_button_id_and_trigger(
        self, page_action: PageAction
    ) -> Tuple[Optional[TriggerActivateEntry], Optional[str]]:
        if self.skip_triggers:
            return None, None
        [action_entry] = self.flow_control_component_next(
            data=to_dict(self.Next(page_action=page_action))
        )
        button_id = generate_button_id()
        trigger = PageButtonTrigger(
            button_id=button_id,
            action=TriggerActionEntry(action_entry.to_typed_dict()),
            text=to_dict(page_action),
        )
        return trigger.activate(), button_id
