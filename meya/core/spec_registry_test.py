import meya
import pytest

from contextlib import ExitStack
from contextlib import asynccontextmanager
from meya.app_config import AppConfig
from meya.app_vault import AppVault
from meya.bot.element import Bot
from meya.button.component.ask import ButtonAskComponent
from meya.core.context import create_load_context
from meya.core.context import create_render_context
from meya.core.source import Source
from meya.core.source_location import SourceLocation
from meya.core.source_registry import SourceRegistry
from meya.core.spec_registry import SpecRegistry
from meya.core.template_registry import TemplateRegistry
from meya.core.type_registry import TypeRegistry
from meya.db.view.db_test import MockDbView
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserView
from meya.element import Ref
from meya.element import Spec
from meya.element import StaticElementProcessor
from meya.element.element_error import ElementImportError
from meya.element.element_error import ElementParseError
from meya.element.element_error import ElementTemplateError
from meya.element.element_error import ElementValidationError
from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_thread
from meya.entry import Entry
from meya.flow.component import FlowComponent
from meya.flow.component.cond import CondComponent
from meya.flow.component.end import EndComponent
from meya.flow.component.if_ import IfComponent
from meya.flow.component.jump import JumpComponent
from meya.flow.component.match import MatchComponent
from meya.flow.component.next import NextComponent
from meya.flow.element import Flow
from meya.freshworks.freshchat.integration import FreshchatIntegration
from meya.google.dialogflow.trigger import DialogflowTrigger
from meya.orb.component.magic_link import OrbMagicLinkComponent
from meya.sensitive_data import SensitiveDataRef
from meya.session.component.chat.open import ChatOpenComponent
from meya.session.trigger.page.open import PageOpenTrigger
from meya.text.component.ask import AskComponent
from meya.text.component.say import SayComponent
from meya.text.trigger.catchall import CatchallTrigger
from meya.text.trigger.keyword import KeywordTrigger
from meya.thread.component.set import ThreadSetComponent
from meya.time.component.delay import DelayComponent
from meya.user.component.set import UserSetComponent
from meya.util.dict import to_dict
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from unittest.mock import MagicMock


@asynccontextmanager
async def _load_app(
    file_path: str,
    text: str,
    *,
    app_config: Optional[AppConfig] = None,
    skip_validate: bool = False,
) -> Tuple[TypeRegistry, SpecRegistry]:
    with ExitStack() as stack:
        app_config = app_config or MagicMock()
        stack.enter_context(AppConfig.current.set(app_config))
        app_vault = MagicMock()
        stack.enter_context(AppVault.current.set(app_vault))
        stack.enter_context(
            StaticElementProcessor.current.set(StaticElementProcessor())
        )
        source_registry = SourceRegistry([Source(file_path, text)])
        stack.enter_context(SourceRegistry.current.set(source_registry))
        context = create_load_context()
        template_registry = await TemplateRegistry.parse_and_try_render(
            context
        )
        stack.enter_context(TemplateRegistry.current.set(template_registry))
        type_registry = TypeRegistry.import_and_index(meya)
        stack.enter_context(TypeRegistry.current.set(type_registry))
        spec_registry = await SpecRegistry.extract()
        stack.enter_context(SpecRegistry.current.set(spec_registry))
        if not skip_validate:
            spec_registry.validate()
        stack.enter_context(MockDbView.current.set(MockDbView()))
        yield spec_registry


def _spec_id(base: str, *parts: Any):
    spec_id = base
    for part in parts:
        spec_id = f"{spec_id}.{part}"
    return spec_id


async def _context(
    flow: Optional[Dict[str, Any]] = None,
    thread: Optional[Dict[str, Any]] = None,
    user: Optional[Dict[str, Any]] = None,
    event_user: Optional[Dict[str, Any]] = None,
):
    with ExitStack() as stack:
        flow_start_entry = create_flow_start_entry(data=flow)
        stack.enter_context(Entry.current.set(flow_start_entry))
        stack.enter_context(Entry.current_encrypted.set(flow_start_entry))
        stack.enter_context(Entry.current_redacted.set(flow_start_entry))
        stack.enter_context(ThreadView.current.set(ThreadView(data=thread)))
        stack.enter_context(UserView.current.set(UserView(data=user)))
        stack.enter_context(
            UserView.event_current.set(UserView(data=event_user))
        )
        return await create_render_context()


async def _flow(**kwargs):
    return await _context(flow=kwargs)


@pytest.mark.asyncio
async def test_bot_ok():
    async with _load_app(
        "bot.yaml",
        "type: meya.bot.element\n"
        "name: Assist\n"
        "avatar:\n"
        "  monogram: A\n",
    ) as spec_registry:
        bot_ref = Ref("bot")
        assert len(spec_registry.items) == 1
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(bot_ref) == Spec(
            type=Bot.get_element_type(),
            data={"name": "Assist", "avatar": {"monogram": "A"}},
            id=bot_ref.ref,
            source_location=SourceLocation(
                file_path="bot.yaml", line=0, column=0
            ),
        )


@pytest.mark.asyncio
async def test_trigger_ok():
    async with _load_app(
        "trigger/a.yaml",
        "id: trigger.a\n"
        "keyword: a\n"
        "action:\n"
        "  flow: flow.a\n"
        "---\n"
        "id: flow.a\n"
        "steps:\n"
        "- say: a\n",
    ) as spec_registry:
        trigger_ref = Ref("trigger.a")
        action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=KeywordTrigger.get_element_type(),
            data={"keyword": "a", "action": {"id": action_ref.ref}},
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="trigger/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": "flow.a"}},
            id=action_ref.ref,
            source_location=SourceLocation(
                file_path="trigger/a.yaml", line=3, column=2
            ),
        )
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="trigger/a.yaml", line=5, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "a"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="trigger/a.yaml", line=7, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_label_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- (start)\n"
        "- type: meya.text.component.say\n"
        "  say: hi\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 1))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [{"step_label": "start"}, {"id": component_ref.ref}]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=3, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_string_ok():
    async with _load_app(
        "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" "- open_chat\n"
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=ChatOpenComponent.get_element_type(),
            data={},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_config_template_jump_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- jump: (@ config.next )\n"
        "- (start)\n",
        app_config=AppConfig(next="start"),
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [{"id": component_ref.ref}, {"step_label": "start"}]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "start"}, "context_flow": {"ref": "flow.a"}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_template_jump_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- jump: (@ flow.next )\n"
        "- (start)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [{"id": component_ref.ref}, {"step_label": "start"}]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(next="start"), component_ref
        ) == Spec(
            type=JumpComponent.get_element_type(),
            data={
                "jump": {"ref": "start"},
                "context_flow": {"ref": flow_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(await _flow(next="x"), component_ref)
        assert str(excinfo.value) == (
            'flow "flow.a" does not have a (x) label\n'
            '  File: "flow/a.yaml", line 3\n'
            "  - jump: (@ flow.next )\n"
            "          ^"
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(
                await _flow(wrong_next="start"), component_ref
            )
        assert str(excinfo.value) == (
            "'meya.core.context.FlowScope object' has no attribute 'next' in JumpComponent.jump template\n"
            '  File: "flow/a.yaml", line 3\n'
            "  - jump: (@ flow.next )\n"
            "          ^"
        )


@pytest.mark.asyncio
async def test_flow_template_call_ok():
    async with _load_app(
        "flow/a.yaml",
        "id: flow.caller\n"
        "steps:\n"
        "- flow: (@ flow.call )\n"
        "---\n"
        "id: flow.callee\n"
        "steps:\n"
        "- say: called\n",
    ) as spec_registry:
        flow_0_ref = Ref("flow.caller")
        component_0_ref = Ref(_spec_id(flow_0_ref.ref, "steps", 0))
        flow_1_ref = Ref("flow.callee")
        component_1_ref = Ref(_spec_id(flow_1_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_0_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_0_ref.ref}]},
            id=flow_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_0_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data=None,
            id=component_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(call=flow_1_ref.ref), component_0_ref
        ) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_1_ref.ref}},
            id=component_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(await _flow(call="x"), component_0_ref)
        assert str(excinfo.value) == (
            'unresolved Flow reference "x"\n'
            '  File: "flow/a.yaml", line 3\n'
            "  - flow: (@ flow.call )\n"
            "          ^"
        )
        assert spec_registry.resolve(flow_1_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_1_ref.ref}]},
            id=flow_1_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=4, column=0
            ),
        )
        assert spec_registry.resolve(component_1_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "called"},
            id=component_1_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_template_call_and_jump_ok():
    async with _load_app(
        "flow/a.yaml",
        "id: flow.caller\n"
        "steps:\n"
        "- flow: (@ flow.call )\n"
        "  jump: (@ flow.jump )\n"
        "---\n"
        "id: flow.callee\n"
        "steps:\n"
        "- (start)\n"
        "- say: called\n",
    ) as spec_registry:
        flow_0_ref = Ref("flow.caller")
        component_0_ref = Ref(_spec_id(flow_0_ref.ref, "steps", 0))
        flow_1_ref = Ref("flow.callee")
        component_1_ref = Ref(_spec_id(flow_1_ref.ref, "steps", 1))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_0_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_0_ref.ref}]},
            id=flow_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_0_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data=None,
            id=component_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(call=flow_1_ref.ref, jump="start"), component_0_ref
        ) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_1_ref.ref}, "jump": {"ref": "start"}},
            id=component_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(call="x", jump="start"), component_0_ref
            )
        assert str(excinfo.value) == (
            'unresolved Flow reference "x"\n'
            '  File: "flow/a.yaml", line 3\n'
            "  - flow: (@ flow.call )\n"
            "          ^"
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(call=flow_1_ref.ref, jump="x"), component_0_ref
            )
        assert str(excinfo.value) == (
            'flow "flow.callee" does not have a (x) label\n'
            '  File: "flow/a.yaml", line 4\n'
            "    jump: (@ flow.jump )\n"
            "          ^"
        )
        assert spec_registry.resolve(flow_1_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [{"step_label": "start"}, {"id": component_1_ref.ref}]
            },
            id=flow_1_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=5, column=0
            ),
        )
        assert spec_registry.resolve(component_1_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "called"},
            id=component_1_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=8, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_dataclass_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- type: meya.text.component.say\n"
        "  say: hi\n"
        "  composer:\n"
        "    visibility: collapse\n"
        "    placeholder: null\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={
                "say": "hi",
                "composer": {"visibility": "collapse", "placeholder": None},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_single_signature_ok():
    async with _load_app(
        "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" "- ask: name?\n"
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=AskComponent.get_element_type(),
            data={"ask": "name?"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_multi_signature_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- if: true\n"
        "  then:\n"
        "    next\n"
        "  else:\n"
        "    end\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        then_action_ref = Ref(_spec_id(component_ref.ref, "then"))
        else_action_ref = Ref(_spec_id(component_ref.ref, "else"))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=IfComponent.get_element_type(),
            data={
                "if_": True,
                "then": {"id": then_action_ref.ref},
                "else_": {"id": else_action_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert spec_registry.resolve(then_action_ref) == Spec(
            type=NextComponent.get_element_type(),
            data={},
            id=then_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=4, column=4
            ),
        )
        assert spec_registry.resolve(else_action_ref) == Spec(
            type=EndComponent.get_element_type(),
            data={},
            id=else_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=4
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_dict_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- match:\n"
        "    a+:\n"
        "      jump: a\n"
        "    ^(bb)+$:\n"
        "      jump: b\n"
        "  default:\n"
        "    jump: c\n"
        "- (a)\n"
        "- (b)\n"
        "- (c)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        match_a_action_ref = Ref(_spec_id(component_ref.ref, "match", "a+"))
        match_b_action_ref = Ref(
            _spec_id(component_ref.ref, "match", "^(bb)+$")
        )
        default_action_ref = Ref(_spec_id(component_ref.ref, "default"))
        assert len(spec_registry.items) == 5
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [
                    {"id": component_ref.ref},
                    {"step_label": "a"},
                    {"step_label": "b"},
                    {"step_label": "c"},
                ]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=MatchComponent.get_element_type(),
            data={
                "match": {
                    "a+": {"id": match_a_action_ref.ref},
                    "^(bb)+$": {"id": match_b_action_ref.ref},
                },
                "default": {"id": default_action_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert spec_registry.resolve(match_a_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "a"}, "context_flow": {"ref": flow_ref.ref}},
            id=match_a_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=4, column=6
            ),
        )
        assert spec_registry.resolve(match_b_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "b"}, "context_flow": {"ref": flow_ref.ref}},
            id=match_b_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=6
            ),
        )
        assert spec_registry.resolve(default_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "c"}, "context_flow": {"ref": flow_ref.ref}},
            id=default_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=8, column=4
            ),
        )


@pytest.mark.asyncio
async def test_flow_component_list_dict_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- cond:\n"
        "    - 0:\n"
        "        jump: a\n"
        "    - 1:\n"
        "        jump: b\n"
        "  default:\n"
        "    jump: c\n"
        "- (a)\n"
        "- (b)\n"
        "- (c)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        cond_0_action_ref = Ref(_spec_id(component_ref.ref, "cond", 0, 0))
        cond_1_action_ref = Ref(_spec_id(component_ref.ref, "cond", 1, 1))
        default_action_ref = Ref(_spec_id(component_ref.ref, "default"))
        assert len(spec_registry.items) == 5
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [
                    {"id": component_ref.ref},
                    {"step_label": "a"},
                    {"step_label": "b"},
                    {"step_label": "c"},
                ]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=CondComponent.get_element_type(),
            data={
                "cond": [
                    {0: {"id": cond_0_action_ref.ref}},
                    {1: {"id": cond_1_action_ref.ref}},
                ],
                "default": {"id": default_action_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert spec_registry.resolve(cond_0_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "a"}, "context_flow": {"ref": flow_ref.ref}},
            id=cond_0_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=4, column=8
            ),
        )
        assert spec_registry.resolve(cond_1_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "b"}, "context_flow": {"ref": flow_ref.ref}},
            id=cond_1_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=8
            ),
        )
        assert spec_registry.resolve(default_action_ref) == Spec(
            type=JumpComponent.get_element_type(),
            data={"jump": {"ref": "c"}, "context_flow": {"ref": flow_ref.ref}},
            id=default_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=8, column=4
            ),
        )


@pytest.mark.parametrize(
    ("flow_line", "say_text"),
    [
        ("- say: Test (@ flow.valid_sensitive )\n", "Test date of birth"),
        ("- say: Test (@ flow['valid_sensitive'] )\n", "Test date of birth"),
        (
            "- say: Test (@ flow.get('valid_sensitive') )\n",
            "Test date of birth",
        ),
        (
            "- say: Test (@ flow.valid_sensitive | encrypt_sensitive )\n",
            "Test {'🔐🙈': 'tz=<zWgu^6AYy59bZ7'}",
        ),
        (
            "- say: Test (@ encrypted_flow.valid_sensitive )\n",
            "Test {'🔐🙈': 'tz=<zWgu^6AYy59bZ7'}",
        ),
        (
            "- say: Test (@ encrypted_flow.valid_sensitive | decrypt_sensitive )\n",
            "Test date of birth",
        ),
        ("- say: Test (@ redacted_flow.valid_sensitive )\n", "Test ⭑⭑⭑⭑⭑⭑"),
        ("- say: Test (@ flow.invalid_sensitive )\n", "Test ⭑⭑⭑⭑⭑⭑"),
        (
            "- say: Test (@ encrypted_flow.invalid_sensitive )\n",
            "Test {'🔐🙈': '::::'}",
        ),
        (
            "- say: Test (@ encrypted_flow.invalid_sensitive | try_decrypt_sensitive('star star') )\n",
            "Test star star",
        ),
        ("- say: Test (@ redacted_flow.invalid_sensitive )\n", "Test ⭑⭑⭑⭑⭑⭑"),
    ],
)
@pytest.mark.asyncio
async def test_flow_encrypt_decrypt(flow_line: str, say_text: str):
    async with _load_app(
        "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" f"{flow_line}"
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert await spec_registry.render(
            await _flow(
                valid_sensitive=to_dict(
                    await MockDbView().encrypt_sensitive("date of birth")
                ),
                invalid_sensitive=to_dict(
                    SensitiveDataRef(ref_key_value="::::")
                ),
            ),
            component_ref,
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": say_text},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.parametrize(
    ("flow_line", "say_text"),
    [
        ("- say: Test (@ thread.valid_sensitive )\n", "Test age"),
        (
            "- say: Test (@ encrypted_thread.valid_sensitive )\n",
            "Test {'🔐🙈': 'qhV)d'}",
        ),
        ("- say: Test (@ redacted_thread.valid_sensitive )\n", "Test ⭑⭑⭑⭑⭑⭑"),
        ("- say: Test (@ thread.normal )\n", "Test abc"),
        ("- say: Test (@ encrypted_thread.normal )\n", "Test abc"),
        ("- say: Test (@ redacted_thread.normal )\n", "Test abc"),
        ("- say: Test (@ thread.invalid )\n", "Test None"),
        ("- say: Test (@ encrypted_thread.invalid )\n", "Test None"),
        ("- say: Test (@ redacted_thread.invalid )\n", "Test None"),
        ("- say: Test (@ user.valid_sensitive )\n", "Test date of birth"),
        (
            "- say: Test (@ encrypted_user.valid_sensitive )\n",
            "Test {'🔐🙈': 'tz=<zWgu^6AYy59bZ7'}",
        ),
        ("- say: Test (@ redacted_user.valid_sensitive )\n", "Test ⭑⭑⭑⭑⭑⭑"),
        ("- say: Test (@ user.normal )\n", "Test xyz"),
        ("- say: Test (@ encrypted_user.normal )\n", "Test xyz"),
        ("- say: Test (@ redacted_user.normal )\n", "Test xyz"),
        ("- say: Test (@ user.invalid )\n", "Test None"),
        ("- say: Test (@ encrypted_user.invalid )\n", "Test None"),
        ("- say: Test (@ redacted_user.invalid )\n", "Test None"),
        (
            "- say: Test (@ event_user.valid_sensitive )\n",
            "Test time of birth",
        ),
        (
            "- say: Test (@ encrypted_event_user.valid_sensitive )\n",
            "Test {'🔐🙈': 't#oN^Wgu^6AYy59bZ7'}",
        ),
        (
            "- say: Test (@ redacted_event_user.valid_sensitive )\n",
            "Test ⭑⭑⭑⭑⭑⭑",
        ),
        ("- say: Test (@ event_user.normal )\n", "Test 123"),
        ("- say: Test (@ encrypted_event_user.normal )\n", "Test 123"),
        ("- say: Test (@ redacted_event_user.normal )\n", "Test 123"),
        ("- say: Test (@ event_user.invalid )\n", "Test None"),
        ("- say: Test (@ encrypted_event_user.invalid )\n", "Test None"),
        ("- say: Test (@ redacted_event_user.invalid )\n", "Test None"),
    ],
)
@pytest.mark.asyncio
async def test_user_thread_decrypt(flow_line: str, say_text: str):
    async with _load_app(
        "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" f"{flow_line}"
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert await spec_registry.render(
            await _context(
                thread=dict(
                    valid_sensitive=to_dict(
                        await MockDbView().encrypt_sensitive("age")
                    ),
                    normal="abc",
                ),
                user=dict(
                    valid_sensitive=to_dict(
                        await MockDbView().encrypt_sensitive("date of birth")
                    ),
                    normal="xyz",
                ),
                event_user=dict(
                    valid_sensitive=to_dict(
                        await MockDbView().encrypt_sensitive("time of birth")
                    ),
                    normal="123",
                ),
            ),
            component_ref,
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": say_text},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_timeout_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- say: hi\n"
        "  timeout: 300\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
            timeout=300,
        )


@pytest.mark.asyncio
async def test_timedelta_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- integration: integration.orb\n"
        "  magic_link: https://example.org\n"
        "  button_id: false\n"
        "  single_use: true\n"
        "  expiry: 61m\n",
        skip_validate=True,
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=OrbMagicLinkComponent.get_element_type(),
            data={
                "integration": {"ref": "integration.orb"},
                "magic_link": "https://example.org",
                "button_id": False,
                "single_use": True,
                "expiry": "1h 1m",
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_str_subclass_ok():
    async with _load_app(
        "integration/a.yaml",
        "type: meya.freshworks.freshchat.integration\n"
        "api_token: x\n"
        "app_id: y\n"
        "bot_agent_email: z\n"
        "assignment_rules:\n"
        "  human_agent: expert\n"
        "  group: bot\n",
    ) as spec_registry:
        integration_ref = Ref("integration.a")
        assert len(spec_registry.items) == 1
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(integration_ref) == Spec(
            type=FreshchatIntegration.get_element_type(),
            data={
                "api_token": "x",
                "app_id": "y",
                "bot_agent_email": "z",
                "assignment_rules": {"human_agent": "expert", "group": "bot"},
            },
            id=integration_ref.ref,
            source_location=SourceLocation(
                file_path="integration/a.yaml", line=0, column=0
            ),
        )


@pytest.mark.asyncio
async def test_flow_simple_trigger_ok():
    async with _load_app(
        "flow/a.yaml", "triggers:\n" "- keyword: hi\n" "steps:\n" "- say: hi\n"
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        trigger_ref = Ref(_spec_id(flow_ref.ref, "triggers", 0))
        trigger_action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "triggers": [{"id": trigger_ref.ref}],
                "steps": [{"id": component_ref.ref}],
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=KeywordTrigger.get_element_type(),
            data={"keyword": "hi", "action": {"id": trigger_action_ref.ref}},
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(trigger_action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_ref.ref}},
            id=trigger_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=3, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_enum_trigger_ok():
    async with _load_app(
        "flow/a.yaml",
        "triggers:\n"
        "- expect: dialogflow\n"
        "  integration: integration.dialogflow\n"
        "  language: en\n"
        "steps:\n"
        "- say: hi\n",
        skip_validate=True,
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        trigger_ref = Ref(_spec_id(flow_ref.ref, "triggers", 0))
        trigger_action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "triggers": [{"id": trigger_ref.ref}],
                "steps": [{"id": component_ref.ref}],
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=DialogflowTrigger.get_element_type(),
            data={
                "expect": "dialogflow",
                "integration": {"ref": "integration.dialogflow"},
                "language": "en",
                "action": {"id": trigger_action_ref.ref},
            },
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(trigger_action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_ref.ref}},
            id=trigger_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=5, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_string_trigger_ok():
    async with _load_app(
        "flow/a.yaml",
        "triggers:\n"
        "- meya.text.trigger.catchall\n"
        "steps:\n"
        "- say: hi\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        trigger_ref = Ref(_spec_id(flow_ref.ref, "triggers", 0))
        trigger_action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "triggers": [{"id": trigger_ref.ref}],
                "steps": [{"id": component_ref.ref}],
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=CatchallTrigger.get_element_type(),
            data={"action": {"id": trigger_action_ref.ref}},
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(trigger_action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_ref.ref}},
            id=trigger_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=3, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_custom_trigger_ok():
    async with _load_app(
        "flow/a.yaml",
        "triggers:\n"
        "- keyword: yo\n"
        "  action: \n"
        "    jump: start\n"
        "    data:\n"
        "      slang: true\n"
        "steps:\n"
        "- (start)\n"
        "- say: hi\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        trigger_ref = Ref(_spec_id(flow_ref.ref, "triggers", 0))
        trigger_action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 1))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 0
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "triggers": [{"id": trigger_ref.ref}],
                "steps": [{"step_label": "start"}, {"id": component_ref.ref}],
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=KeywordTrigger.get_element_type(),
            data={"keyword": "yo", "action": {"id": trigger_action_ref.ref}},
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(trigger_action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={
                "jump": {"ref": "start"},
                "data": {"slang": True},
                "flow": {"ref": flow_ref.ref},
            },
            id=trigger_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=3, column=4
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=8, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_dynamic_trigger_ok():
    async with _load_app(
        "flow/a.yaml",
        "triggers:\n"
        "- type: page_open\n"
        "  when: (@ not thread.open_page )\n"
        "\n"
        "steps:\n"
        "- say: Hey, welcome!\n"
        "- thread_set:\n"
        "    open_page: true\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        trigger_ref = Ref(_spec_id(flow_ref.ref, "triggers", 0))
        trigger_action_ref = Ref(_spec_id(trigger_ref.ref, "action"))
        component_0_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        component_1_ref = Ref(_spec_id(flow_ref.ref, "steps", 1))
        assert len(spec_registry.items) == 5
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={
                "triggers": [{"id": trigger_ref.ref}],
                "steps": [
                    {"id": component_0_ref.ref},
                    {"id": component_1_ref.ref},
                ],
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(trigger_ref) == Spec(
            type=PageOpenTrigger.get_element_type(),
            data=None,
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert await spec_registry.render(
            dict(thread=create_thread("t0")), trigger_ref
        ) == Spec(
            type=PageOpenTrigger.get_element_type(),
            data={"action": {"id": trigger_action_ref.ref}, "when": True},
            id=trigger_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(trigger_action_ref) == Spec(
            type=FlowComponent.get_element_type(),
            data={"flow": {"ref": flow_ref.ref}},
            id=trigger_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=1, column=2
            ),
        )
        assert spec_registry.resolve(component_0_ref) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "Hey, welcome!"},
            id=component_0_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=5, column=2
            ),
        )
        assert spec_registry.resolve(component_1_ref) == Spec(
            type=ThreadSetComponent.get_element_type(),
            data={"thread_set": {"open_page": True}},
            id=component_1_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_string_template_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n" "steps:\n" "- say: Hi (@ flow.name )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(name="Ada"), component_ref
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "Hi Ada"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(dict(), component_ref)
        assert str(excinfo.value) == (
            "'flow' is undefined in SayComponent.say template\n"
            '  File: "flow/a.yaml", line 3\n'
            "  - say: Hi (@ flow.name )\n"
            "         ^"
        )


@pytest.mark.asyncio
async def test_flow_none_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- say: (@ flow.get('greeting') )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(greeting="hi"), component_ref
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi"},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(), component_ref
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": None},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_string_type_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n" "steps:\n" "- delay: (@ flow.result )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=DelayComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(result="text"), component_ref
            )
        assert str(excinfo.value) == (
            "not a valid Real for DelayComponent.delay\n"
            '  File: "flow/a.yaml", line 3\n'
            "  - delay: (@ flow.result )\n"
            "           ^"
        )


@pytest.mark.asyncio
async def test_flow_nested_string_type_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- buttons:\n"
        "  - (@ flow.result )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        button_action_ref = Ref(
            _spec_id(component_ref.ref, "buttons", 0, "action")
        )
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=ButtonAskComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(result={"text": "go", "action": "next"}), component_ref
        ) == Spec(
            type=ButtonAskComponent.get_element_type(),
            data={
                "buttons": [
                    {
                        "text": "go",
                        "action": {
                            "type": NextComponent.get_element_type(),
                            "data": {},
                            "id": button_action_ref.ref,
                            "source_location": {
                                "file_path": "flow/a.yaml",
                                "line": 3,
                                "column": 4,
                            },
                        },
                    }
                ]
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(result={"text": 2, "action": "next"}),
                component_ref,
            )
        assert str(excinfo.value) == (
            "not a valid str for ButtonElementSpec.text\n"
            '  File: "flow/a.yaml", line 4\n'
            "    - (@ flow.result )\n"
            "      ^"
        )


@pytest.mark.asyncio
async def test_flow_nested_key_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- buttons:\n"
        "  - (@ flow.result )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=ButtonAskComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(result={"a": "b"}), component_ref
            )
        assert str(excinfo.value) == (
            'unexpected key "a" for ButtonElementSpec\n'
            '  File: "flow/a.yaml", line 4\n'
            "    - (@ flow.result )\n"
            "      ^"
        )


@pytest.mark.asyncio
async def test_flow_spec_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n" "steps:\n" "- (@ flow.result )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        assert len(spec_registry.items) == 1
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data=None,
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(result={"a": "b"}), flow_ref
            )
        assert str(excinfo.value) == (
            "not a valid StepLabel or FlowComponentSpec for Flow.steps\n"
            '  File: "flow/a.yaml", line 3\n'
            "  - (@ flow.result )\n"
            "    ^"
        )


@pytest.mark.asyncio
async def test_flow_template_dict_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- user_set:\n"
        "    email_dict: (@ flow.result )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=UserSetComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(result={"key": "value"}), component_ref
        ) == Spec(
            type=UserSetComponent.get_element_type(),
            data={"user_set": {"email_dict": {"key": "value"}}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(result={"key": "value"}), component_ref
        ) == Spec(
            type=UserSetComponent.get_element_type(),
            data={"user_set": {"email_dict": {"key": "value"}}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_template_step_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n" "steps:\n" "- (@ flow.step )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 1
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data=None,
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert await spec_registry.render(
            await _flow(step={"say": "hi"}), flow_ref
        ) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [
                    {
                        "type": SayComponent.get_element_type(),
                        "data": {"say": "hi"},
                        "id": component_ref.ref,
                        "source_location": {
                            "file_path": "flow/a.yaml",
                            "line": 2,
                            "column": 2,
                        },
                    }
                ]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert await spec_registry.render(
            await _flow(step={"say": "hi"}), flow_ref
        ) == Spec(
            type=Flow.get_element_type(),
            data={
                "steps": [
                    {
                        "type": SayComponent.get_element_type(),
                        "data": {"say": "hi"},
                        "id": component_ref.ref,
                        "source_location": {
                            "file_path": "flow/a.yaml",
                            "line": 2,
                            "column": 2,
                        },
                    }
                ]
            },
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )


@pytest.mark.asyncio
async def test_flow_template_list_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- ask: Colour?\n"
        "  quick_replies: (@ flow.colours )\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=AskComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(colours=["red", "green", "blue"]), component_ref
        ) == Spec(
            type=AskComponent.get_element_type(),
            data={"ask": "Colour?", "quick_replies": ["red", "green", "blue"]},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(colours=["red", "green", "blue"]), component_ref
        ) == Spec(
            type=AskComponent.get_element_type(),
            data={"ask": "Colour?", "quick_replies": ["red", "green", "blue"]},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )


@pytest.mark.asyncio
async def test_flow_any_template_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- user_set:\n"
        "    email_dict: (@ flow.email)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=UserSetComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(email="abc@xyz.com"), component_ref
        ) == Spec(
            type=UserSetComponent.get_element_type(),
            data={"user_set": {"email_dict": "abc@xyz.com"}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(email="abc@xyz.com"), component_ref
        ) == Spec(
            type=UserSetComponent.get_element_type(),
            data={"user_set": {"email_dict": "abc@xyz.com"}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(dict(), component_ref)
        assert str(excinfo.value) == (
            "'flow' is undefined in UserSetComponent.user_set template\n"
            '  File: "flow/a.yaml", line 4\n'
            "      email_dict: (@ flow.email)\n"
            "                  ^"
        )


@pytest.mark.asyncio
async def test_flow_number_template_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n" "steps:\n" "- delay: (@ flow.delay)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=DelayComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(delay=2), component_ref
        ) == Spec(
            type=DelayComponent.get_element_type(),
            data={"delay": 2},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(delay=2), component_ref
        ) == Spec(
            type=DelayComponent.get_element_type(),
            data={"delay": 2},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(dict(), component_ref)
        assert str(excinfo.value) == (
            "'flow' is undefined in DelayComponent.delay template\n"
            '  File: "flow/a.yaml", line 3\n'
            "  - delay: (@ flow.delay)\n"
            "           ^"
        )


@pytest.mark.asyncio
async def test_flow_complex_template_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- say: hi\n"
        "  composer: (@ flow.composer)\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        assert len(spec_registry.items) == 2
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=SayComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(composer=dict(focus="blur")), component_ref
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi", "composer": {"focus": "blur"}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(composer=dict(focus="blur")), component_ref
        ) == Spec(
            type=SayComponent.get_element_type(),
            data={"say": "hi", "composer": {"focus": "blur"}},
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(composer=dict(focus="x")), component_ref
            )
        assert str(excinfo.value) == (
            "not a valid ComposerFocus for ComposerElementSpec.focus\n"
            '  File: "flow/a.yaml", line 4\n'
            "    composer: (@ flow.composer)\n"
            "              ^"
        )
        with pytest.raises(ElementValidationError) as excinfo:
            await spec_registry.render(
                await _flow(composer="y"), component_ref
            )
        assert str(excinfo.value) == (
            "not a valid ComposerElementSpec for SayComponent.composer\n"
            '  File: "flow/a.yaml", line 4\n'
            "    composer: (@ flow.composer)\n"
            "              ^"
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(dict(), component_ref)
        assert str(excinfo.value) == (
            "'flow' is undefined in SayComponent.composer template\n"
            '  File: "flow/a.yaml", line 4\n'
            "    composer: (@ flow.composer)\n"
            "              ^"
        )


@pytest.mark.asyncio
async def test_flow_dict_key_template_error_ok():
    async with _load_app(
        "flow/a.yaml",
        "type: meya.flow.element\n"
        "steps:\n"
        "- cond:\n"
        "    - (@ not flow.ok ):\n"
        "        end\n"
        "  default:\n"
        "    end\n",
    ) as spec_registry:
        flow_ref = Ref("flow.a")
        component_ref = Ref(_spec_id(flow_ref.ref, "steps", 0))
        cond_action_ref = Ref(
            f'{_spec_id(component_ref.ref, "cond", 0)}:index.0'
        )
        default_action_ref = Ref(_spec_id(component_ref.ref, "default"))
        assert len(spec_registry.items) == 4
        assert len(spec_registry.template_items) == 1
        assert spec_registry.resolve(flow_ref) == Spec(
            type=Flow.get_element_type(),
            data={"steps": [{"id": component_ref.ref}]},
            id=flow_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=0, column=0
            ),
        )
        assert spec_registry.resolve(component_ref) == Spec(
            type=CondComponent.get_element_type(),
            data=None,
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(ok=True), component_ref
        ) == Spec(
            type=CondComponent.get_element_type(),
            data={
                "cond": [{False: {"id": cond_action_ref.ref}}],
                "default": {"id": default_action_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        assert await spec_registry.render(
            await _flow(ok=True), component_ref
        ) == Spec(
            type=CondComponent.get_element_type(),
            data={
                "cond": [{False: {"id": cond_action_ref.ref}}],
                "default": {"id": default_action_ref.ref},
            },
            id=component_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=2, column=2
            ),
        )
        with pytest.raises(ElementTemplateError) as excinfo:
            await spec_registry.render(dict(), component_ref)
        assert str(excinfo.value) == (
            "'flow' is undefined in CondComponent.cond template\n"
            '  File: "flow/a.yaml", line 4\n'
            "      - (@ not flow.ok ):\n"
            "        ^"
        )
        assert spec_registry.resolve(cond_action_ref) == Spec(
            type=EndComponent.get_element_type(),
            data={},
            id=cond_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=4, column=8
            ),
        )
        assert spec_registry.resolve(default_action_ref) == Spec(
            type=EndComponent.get_element_type(),
            data={},
            id=default_action_ref.ref,
            source_location=SourceLocation(
                file_path="flow/a.yaml", line=6, column=4
            ),
        )


@pytest.mark.asyncio
async def test_missing_id_error():
    with pytest.raises(ElementParseError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "id: i\n"
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "---\n"
            "q: r\n",
        ):
            pass
    assert str(excinfo.value) == (
        "'id' required for multi-document YAML files\n"
        '  File: "flow/a.yaml", line 7\n'
        "  q: r\n"
        "  ^"
    )


@pytest.mark.asyncio
async def test_invalid_type_error():
    with pytest.raises(ElementImportError) as excinfo:
        async with _load_app("flow/a.yaml", "type: meya.flowx"):
            pass
    assert str(excinfo.value) == (
        'no such element type "meya.flowx"\n'
        '  File: "flow/a.yaml", line 1\n'
        "  type: meya.flowx\n"
        "        ^"
    )


@pytest.mark.asyncio
async def test_invalid_string_type_error():
    with pytest.raises(ElementImportError) as excinfo:
        async with _load_app(
            "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" "- endx\n"
        ):
            pass
    assert str(excinfo.value) == (
        'no such element "endx"\n'
        '  File: "flow/a.yaml", line 3\n'
        "  - endx\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_invalid_root_element_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app("flow/a.yaml", "x: y"):
            pass
    assert str(excinfo.value) == (
        "not a valid Spec\n" '  File: "flow/a.yaml", line 1\n' "  x: y\n" "  ^"
    )


@pytest.mark.asyncio
async def test_invalid_flow_component_yaml_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml", "type: meya.flow.element\n" "steps:\n" "- 1"
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid StepLabel or FlowComponentSpec for Flow.steps\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - 1\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_invalid_flow_component_signature_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n" "steps:\n" "- sayx: hi\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid StepLabel or FlowComponentSpec for Flow.steps\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - sayx: hi\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_missing_key_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n",
        ):
            pass
    assert str(excinfo.value) == (
        'missing key "say" for SayComponent\n'
        '  File: "flow/a.yaml", line 3\n'
        "  - type: meya.text.component.say\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_missing_key_string_type_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- meya.text.component.say\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid StepLabel or FlowComponentSpec for Flow.steps\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - meya.text.component.say\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_extra_key_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "  say2: hi2\n",
        ):
            pass
    assert str(excinfo.value) == (
        'unexpected key "say2" for SayComponent\n'
        '  File: "flow/a.yaml", line 5\n'
        "    say2: hi2\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_extra_template_key_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "  (@ 'say2' ): hi\n",
        ):
            pass
    assert str(excinfo.value) == (
        'unexpected key "say2" for SayComponent\n'
        '  File: "flow/a.yaml", line 5\n'
        "    (@ 'say2' ): hi\n"
        "    ^"
    )


@pytest.mark.asyncio
async def test_dataclass_extra_key_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "  composer:\n"
            "    visibilityx: collapse\n"
            "    placeholder: null\n",
        ):
            pass
    assert str(excinfo.value) == (
        'unexpected key "visibilityx" for ComposerElementSpec\n'
        '  File: "flow/a.yaml", line 6\n'
        "      visibilityx: collapse\n"
        "      ^"
    )


@pytest.mark.asyncio
async def test_invalid_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: 2\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid str for SayComponent.say\n"
        '  File: "flow/a.yaml", line 4\n'
        "    say: 2\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_invalid_template_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: (@ 2 )\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid str for SayComponent.say\n"
        '  File: "flow/a.yaml", line 4\n'
        "    say: (@ 2 )\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_invalid_timeout_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "  timeout: x\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid int for Spec.timeout\n"
        '  File: "flow/a.yaml", line 5\n'
        "    timeout: x\n"
        "             ^"
    )


@pytest.mark.asyncio
async def test_invalid_timeout_template_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  say: hi\n"
            "  timeout: (@ flow.timeout )\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid int for Spec.timeout\n"
        '  File: "flow/a.yaml", line 5\n'
        "    timeout: (@ flow.timeout )\n"
        "             ^"
    )


@pytest.mark.asyncio
async def test_invalid_nested_spec_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- if: true\n"
            "  then:\n"
            "    type: meya.text.component.say\n"
            "    say: 2\n"
            "  else:\n"
            "    end\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid str for SayComponent.say\n"
        '  File: "flow/a.yaml", line 6\n'
        "      say: 2\n"
        "           ^"
    )


@pytest.mark.asyncio
async def test_invalid_nested_spec_outer_template_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- if: (@ flow.ok )\n"
            "  then:\n"
            "    type: meya.text.component.say\n"
            "    say: 2\n"
            "  else:\n"
            "    end\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid str for SayComponent.say\n"
        '  File: "flow/a.yaml", line 6\n'
        "      say: 2\n"
        "           ^"
    )


@pytest.mark.asyncio
async def test_invalid_sibling_template_value_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- type: meya.text.component.say\n"
            "  (@ flow.key ): value\n"
            "  say: 2\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid str for SayComponent.say\n"
        '  File: "flow/a.yaml", line 5\n'
        "    say: 2\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_invalid_ref_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "trigger/a.yaml",
            "id: trigger.a\n"
            "keyword: a\n"
            "action:\n"
            "  flow: flow.b\n"
            "---\n"
            "id: flow.a\n"
            "steps:\n"
            "- say: a\n",
        ):
            pass
    assert str(excinfo.value) == (
        'unresolved Flow reference "flow.b"\n'
        '  File: "trigger/a.yaml", line 4\n'
        "    flow: flow.b\n"
        "          ^"
    )


@pytest.mark.asyncio
async def test_invalid_ref_type_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "trigger/a.yaml",
            "id: trigger.a\n"
            "keyword: a\n"
            "action:\n"
            "  flow: flow.a\n"
            "---\n"
            "id: flow.a\n"
            "keyword: a\n"
            "action:\n"
            "  say: a\n",
        ):
            pass
    assert str(excinfo.value) == (
        '"flow.a" reference is a KeywordTrigger not a Flow\n'
        '  File: "trigger/a.yaml", line 4\n'
        "    flow: flow.a\n"
        "          ^"
    )


@pytest.mark.asyncio
async def test_wrong_action_indent_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- match:\n"
            "    a+:\n"
            "      jump: a\n"
            "    ^(bb)+$:\n"
            "    jump: b\n"
            "  default:\n"
            "    jump: c\n",
        ):
            pass
    # TODO Submit a ruamel patch to get a better location for implicit "null"
    assert str(excinfo.value) == (
        "missing ActionComponentSpec for MatchComponent.match\n"
        '  File: "flow/a.yaml", line 7\n'
        "      jump: b\n"
        "      ^"
    )


@pytest.mark.asyncio
async def test_flow_string_general_template_load_error():
    with pytest.raises(ElementTemplateError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n" "steps:\n" "- say: (@ 1 / 0 )\n",
        ):
            pass
    assert str(excinfo.value) == (
        "division by zero in SayComponent.say template\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - say: (@ 1 / 0 )\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_flow_string_config_template_load_error():
    with pytest.raises(ElementTemplateError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- say: (@ config.missing )\n",
            app_config=AppConfig(valid="VALID"),
        ):
            pass
    assert str(excinfo.value) == (
        "'meya.app_config.AppConfig object' has no attribute 'missing' in SayComponent.say template\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - say: (@ config.missing )\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_flow_string_nested_config_template_load_error():
    with pytest.raises(ElementTemplateError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- say: (@ config.valid.missing )\n",
            app_config=AppConfig(valid=dict(nested_valid="VALID")),
        ):
            pass
    assert str(excinfo.value) == (
        "'dict object' has no attribute 'missing' in SayComponent.say template\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - say: (@ config.valid.missing )\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_flow_string_missing_context_template_load_error():
    with pytest.raises(ElementTemplateError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n" "steps:\n" "- say: (@ missing )\n",
            app_config=AppConfig(valid=dict(nested_valid="VALID")),
        ):
            pass
    assert str(excinfo.value) == (
        "'missing' is undefined in SayComponent.say template\n"
        '  File: "flow/a.yaml", line 3\n'
        "  - say: (@ missing )\n"
        "         ^"
    )


@pytest.mark.asyncio
async def test_invalid_timedelta_error():
    with pytest.raises(ElementValidationError) as excinfo:
        async with _load_app(
            "flow/a.yaml",
            "type: meya.flow.element\n"
            "steps:\n"
            "- integration: integration.orb\n"
            "  magic_link: https://example.org\n"
            "  button_id: b-1\n"
            "  single_use: true\n"
            "  expiry: 3dw\n",
        ):
            pass
    assert str(excinfo.value) == (
        "not a valid timedelta for OrbMagicLinkComponent.expiry\n"
        '  File: "flow/a.yaml", line 7\n'
        "    expiry: 3dw\n"
        "            ^"
    )
