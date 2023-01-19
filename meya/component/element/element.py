from dataclasses import MISSING
from dataclasses import dataclass
from meya.button.spec import AbstractButtonElementSpec
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonElementSpecUnion
from meya.button.spec import ButtonEventSpec
from meya.button.spec import ButtonResultList
from meya.component.element.mixin import FlowControlMixin
from meya.component.entry.next import ComponentNextEntry
from meya.component.entry.start import ComponentStartEntry
from meya.component.spec import AbstractComponent
from meya.core.meta_level import MetaLevel
from meya.element import Ref
from meya.element import Spec
from meya.element.element_error import ElementProcessError
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.event.entry import Event
from meya.icon.spec import IconElementSpecUnion
from meya.trigger.element import ComponentTriggerSpec
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerActionEntry
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.util.dict import from_dict
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

T = TypeVar("T")


@dataclass
class ComponentResponse:
    result: Any = response_field(sensitive=True)


@dataclass
class ComponentOkResponse:
    result: Any = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class ComponentErrorResponse:
    result: Any = response_field(sensitive=True)
    retry_count: int = response_field()
    ok: bool = response_field(default=False)


@dataclass
class Component(AbstractComponent, FlowControlMixin):
    """
    This is the base component element that is used by **all** other component
    elements.

    This is an **abstract** element and should **not** be used directly in
    your BFML.

    When you implement your own [custom components](https://docs.meya.ai/docs/getting-started-with-custom-components)
    you will inherit from this element's Python class.
    """

    OK_KEY: ClassVar[str] = "ok"
    RETRY_COUNT_KEY: ClassVar[str] = "retry_count"

    is_abstract: bool = meta_field(value=True)
    meta_icon: IconElementSpecUnion = meta_field(
        value="streamline-regular/04-programing-apps-websites/02-plugins-modules/module-three-1.svg"
    )

    context: Dict[str, Any] = element_field(
        default_factory=dict,
        help="Send context data with this component's event.",
        level=MetaLevel.ADVANCED,
    )
    sensitive: bool = element_field(
        default=False,
        help=(
            "Mark this component's event as sensitive. This will encrypt the "
            "event if the [Sensitive Data](https://docs.meya.ai/docs/how-to-set-up-the-sensitive-data-integration) "
            "integration has been enabled."
        ),
        level=MetaLevel.ADVANCED,
    )
    triggers: Optional[List[ComponentTriggerSpec]] = element_field(
        default_factory=list,
        help=(
            "Activate these dynamic triggers when the component runs. Check "
            "the [component triggers guide](https://docs.meya.ai/docs/component-triggers) "
            "for more info."
        ),
        level=MetaLevel.ADVANCED,
    )

    start_entry: Optional[ComponentStartEntry] = process_field()
    next_entry: Optional[ComponentNextEntry] = process_field()
    resolved_triggers: List[Spec] = process_field()
    respond_data: Any = process_field()

    def __post_init__(self):
        super().__post_init__()
        self.start_entry = (
            self.entry if isinstance(self.entry, ComponentStartEntry) else None
        )
        self.next_entry = (
            self.entry if isinstance(self.entry, ComponentNextEntry) else None
        )
        self.respond_data = MISSING
        self.resolved_triggers = []

    async def process(self) -> List[Entry]:
        if self.start_entry:
            results = await self.start()
        elif self.next_entry:
            results = await self.next()
        else:
            results = []

        if self.respond_data is not MISSING:
            self.respond_data = await self.encrypt_sensitive_respond_data(
                self.respond_data
            )

        if not self.skip_triggers:
            for trigger in self.triggers:
                if trigger.is_partial:
                    trigger = self.resolve_spec(Ref(trigger.id))
                if trigger.is_partial:
                    trigger = await self.render_spec_data(trigger)
                self.resolved_triggers.append(trigger)

        return results

    async def encrypt_sensitive_respond_data(self, respond_data: T) -> T:
        if (
            self.sensitive or self.get_sensitive_override()
        ) and self.db.config.event_ledger.sensitive_ttl:
            return await self.db.encrypt_sensitive_fields(
                respond_data, preserve_nones=True
            )
        else:
            return respond_data

    def get_sensitive_override(self) -> bool:
        if self.next_entry:
            try:
                event = Entry.from_typed_dict(self.entry.data["event"])
                return event.sensitive
            except (ValueError, KeyError):
                pass
        return False

    async def start(self) -> List[Entry]:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    async def next(self) -> List[Entry]:
        input_result = from_dict(ComponentOkResponse, self.entry.data)
        return self.respond(data=input_result)

    def respond(self, *entries: Entry, data: Any = None) -> List[Entry]:
        self.respond_data = data
        return list(entries)

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        super().post_process(entry, extra_entries)

        if isinstance(entry, Event):
            if entry.context is MISSING:
                entry.context = self.context

    def post_process_all(self, entries: List[Entry]) -> List[Entry]:
        from meya.trigger.entry.activate import TriggerActivateEntry

        entries = super().post_process_all(entries)

        if not self.next_entry or any(
            isinstance(entry, TriggerActivateEntry) for entry in entries
        ):
            for trigger in self.resolved_triggers:
                if not trigger.data or "action" not in trigger.data:
                    raise ElementProcessError(
                        self.source_location,
                        f"{type(self).__name__}.post_process_all() partial trigger spec: {trigger}",
                    )

                entries.append(
                    TriggerActivateEntry(
                        spec=dict(
                            data={
                                **trigger.data,
                                "action": TriggerActionEntry(
                                    entry=self.flow_control_action(
                                        trigger.data["action"]
                                    )[0].to_typed_dict()
                                ),
                            },
                            type=trigger.type,
                        )
                    )
                )

        if (
            self.respond_data is not MISSING
            and self.entry.flow
            and not any(
                isinstance(entry, TriggerActivateEntry) for entry in entries
            )
        ):
            return [*entries, *self.flow_control_next(self.respond_data)]

        # TODO splice data into activate triggers
        assert self.respond_data is None or self.respond_data is MISSING
        return [*entries]

    def reset(self):
        if Trigger.RESULT_KEY in self.entry.data:
            del self.entry.data[Trigger.RESULT_KEY]
        if self.OK_KEY in self.entry.data:
            del self.entry.data[self.OK_KEY]
        if self.RETRY_COUNT_KEY in self.entry.data:
            del self.entry.data[self.RETRY_COUNT_KEY]

    def get_buttons_and_triggers(
        self, buttons: List[ButtonElementSpecUnion]
    ) -> ButtonResultList:
        (
            button_results,
            triggers,
        ) = ButtonEventSpec.from_element_spec_union_list(buttons)
        return ButtonResultList(triggers, button_results)

    def get_button_and_trigger(
        self, button: AbstractButtonElementSpec
    ) -> Tuple[Optional[TriggerActivateEntry], ButtonEventSpec]:
        assert isinstance(button, ButtonElementSpec)
        button_result, triggers = ButtonEventSpec.from_element_spec_union(
            button
        )
        assert button_result is not None
        assert len(triggers) <= 1
        return button_result, (triggers[0] if triggers else None)

    def get_next_action(self, *, data: Any = None) -> TriggerActionEntry:
        [action_entry] = self.flow_control_component_next(data)
        return TriggerActionEntry(action_entry.to_typed_dict())

    @property
    def skip_triggers(self) -> bool:
        return False
