from dataclasses import dataclass
from meya.bot.element import Bot
from meya.bot.element import BotRef
from meya.component.entry import ComponentEntry
from meya.component.entry.next import ComponentNextEntry
from meya.component.entry.start import ComponentStartEntry
from meya.component.spec import ComponentSpec
from meya.element import Element
from meya.element.field import meta_field
from meya.entry import Entry
from meya.flow.element import FlowRef
from meya.flow.element import StepLabelRef
from meya.flow.entry import FlowEntry
from meya.flow.entry.end import FlowEndEntry
from meya.flow.entry.jump import FlowJumpEntry
from meya.flow.entry.next import FlowNextEntry
from meya.flow.entry.start import FlowStartEntry
from meya.flow.stack_frame import StackFrame
from meya.util.dict import to_dict
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class FlowControlMixin(Element):
    is_abstract: bool = meta_field(value=True)

    @classmethod
    def flow_control_start(
        cls,
        flow: FlowRef,
        label: Optional[StepLabelRef] = None,
        data: Any = None,
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        if entry.flow:
            current_stack_frame = StackFrame(
                data=entry.data, flow=entry.flow, index=entry.index
            )
            stack = [current_stack_frame, *entry.stack]
            data = cls.start_data(data)
        else:
            stack = []
            data = cls.next_data(data)
        start_entry = FlowStartEntry(
            bot_id=Bot.get_current_id(),
            data=data,
            flow=flow.ref,
            label=label.ref if label else None,
            stack=stack,
            thread_id=entry.thread_id,
        )
        return [start_entry]

    @classmethod
    def flow_control_start_async(
        cls,
        flow: FlowRef,
        label: Optional[StepLabelRef] = None,
        data: Any = None,
        bot: Optional[BotRef] = None,
        thread_id: Optional[str] = None,
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        data = cls.start_data(data)
        start_entry = FlowStartEntry(
            bot_id=bot.ref if bot else Bot.get_current_id(),
            data=data,
            flow=flow.ref,
            label=label.ref if label else None,
            stack=[],
            thread_id=thread_id or entry.thread_id,
        )
        return [start_entry, *cls.flow_control_next()]

    @classmethod
    def flow_control_next(cls, data: Any = None) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        assert entry.flow is not None
        next_entry = FlowNextEntry(
            bot_id=Bot.get_current_id(),
            data=cls.next_data(data),
            flow=entry.flow,
            index=entry.index,
            stack=entry.stack,
            thread_id=entry.thread_id,
        )
        return [next_entry]

    @classmethod
    def flow_control_component_next(cls, data: Any = None) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, ComponentEntry)
        next_entry = ComponentNextEntry(
            bot_id=entry.bot_id,
            data=cls.next_data(data),
            flow=entry.flow,
            index=entry.index,
            spec=entry.spec,
            stack=entry.stack,
            thread_id=entry.thread_id,
        )
        return [next_entry]

    @classmethod
    def flow_control_jump(
        cls, label: StepLabelRef, data: Any = None
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        assert entry.flow is not None
        jump_entry = FlowJumpEntry(
            bot_id=Bot.get_current_id(),
            data=cls.next_data(data),
            flow=entry.flow,
            label=label.ref,
            stack=entry.stack,
            thread_id=entry.thread_id,
        )
        return [jump_entry]

    @classmethod
    def flow_control_jump_start(
        cls,
        flow: FlowRef,
        label: Optional[StepLabelRef] = None,
        data: Any = None,
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        assert entry.flow is not None
        jump_start_entry = FlowStartEntry(
            bot_id=Bot.get_current_id(),
            data=cls.start_data(data),
            flow=flow.ref,
            label=label.ref if label else None,
            stack=entry.stack,
            thread_id=entry.thread_id,
        )
        return [jump_start_entry]

    @classmethod
    def flow_control_end(
        cls, data: Any = None, index: Optional[int] = 0
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        assert entry.flow is not None
        stack = entry.stack
        end_entry = FlowEndEntry(
            bot_id=Bot.get_current_id(),
            data=data or {},
            flow=entry.flow,
            index=entry.index if index is None else index,
            stack=stack,
            thread_id=entry.thread_id,
        )
        if len(stack) == 0:
            return [end_entry]

        previous_stack_frame = stack[0]
        data = cls.add_data(previous_stack_frame.data, data)
        next_entry = FlowNextEntry(
            bot_id=Bot.get_current_id(),
            data=data,
            flow=previous_stack_frame.flow,
            index=previous_stack_frame.index,
            stack=stack[1:],
            thread_id=entry.thread_id,
        )
        return [next_entry, end_entry]

    @classmethod
    def flow_control_action(
        cls, action: ComponentSpec, data: Any = None
    ) -> List[Entry]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        assert entry.flow is not None
        start_entry = ComponentStartEntry(
            bot_id=Bot.get_current_id(),
            data=cls.next_data(data),
            flow=entry.flow,
            index=entry.index,
            spec=to_dict(action),
            stack=entry.stack,
            thread_id=entry.thread_id,
        )
        return [start_entry]

    @classmethod
    def start_data(cls, data: Any) -> Dict[str, Any]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        return cls.add_data({}, data)

    @classmethod
    def next_data(cls, data: Any) -> Dict[str, Any]:
        entry = Entry.current.get()
        assert isinstance(entry, (ComponentEntry, FlowEntry))
        return cls.add_data(entry.data, data)

    @staticmethod
    def add_data(initial_data: Dict[str, Any], data: Any) -> Dict[str, Any]:
        if data is None:
            return initial_data
        else:
            return {**initial_data, **to_dict(data, preserve_nones=True)}
