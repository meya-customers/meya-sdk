import asyncio
import meya
import meya.util.uuid

from contextlib import ExitStack
from contextlib import nullcontext
from dataclasses import MISSING
from freezegun import freeze_time
from meya.app_config import AppConfig
from meya.app_vault import AppVault
from meya.bot.element import Bot
from meya.bot.entry import BotEntry
from meya.component.element import Component
from meya.component.entry import ComponentEntry
from meya.component.entry.next import ComponentNextEntry
from meya.component.entry.start import ComponentStartEntry
from meya.component.spec import ComponentSpec
from meya.core.source_registry import SourceRegistry
from meya.core.spec_registry import SpecRegistry
from meya.core.type_registry import TypeRegistry
from meya.db.view.db import DbView
from meya.db.view.db_test import MockDbView
from meya.db.view.http import HttpView
from meya.db.view.http_test import MockHttpView
from meya.db.view.log import LogView
from meya.db.view.log_test import MockLogView
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserType
from meya.db.view.user import UserView
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element import StaticElementProcessor
from meya.entry import Entry
from meya.env_test import patch_env
from meya.event.entry import Event
from meya.flow.element import Flow
from meya.flow.entry.next import FlowNextEntry
from meya.flow.entry.start import FlowStartEntry
from meya.flow.stack_frame import StackFrame
from meya.http.direction import Direction
from meya.http.entry import HttpEntry
from meya.http.entry.request import HttpRequestEntry
from meya.http.entry.response import HttpResponseEntry
from meya.http.entry.ws_upgrade import HttpWsUpgradeEntry
from meya.integration.element import Integration
from meya.log.entry.message import LogMessageEntry
from meya.log.level import Level
from meya.log.scope import Scope
from meya.text.event.say import SayEvent
from meya.thread.entry.data import ThreadDataEntry
from meya.thread.entry.link import ThreadLinkEntry
from meya.thread.entry.unlink import ThreadUnlinkEntry
from meya.time.time import from_utc_milliseconds_timestamp
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerActionEntry
from meya.trigger.element import TriggerSpec
from meya.trigger.entry.activate import TriggerActivateEntry
from meya.trigger.entry.match import TriggerMatchEntry
from meya.user.entry.data import UserDataEntry
from meya.user.entry.link import UserLinkEntry
from meya.user.entry.unlink import UserUnlinkEntry
from meya.util.dict import to_dict
from meya.util.generate_id import generate_thread_id
from meya.util.generate_id import generate_user_id
from meya.util.latency.stats import LatencyStats
from meya.util.test import is_root_cwd
from meya.util.uuid_test import patch_uuid4_hex
from numbers import Real
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from unittest.mock import MagicMock

frozen_milliseconds_timestamp = 1561492810010

try:
    if not is_root_cwd():
        raise ImportError()

    import meya_private

    from grid_private.private_env_test import patch_private_env

    test_type_registry = TypeRegistry.import_and_index(meya, meya_private)
except ImportError:
    meya_private = None
    patch_private_env = nullcontext
    test_type_registry = TypeRegistry.import_and_index_for_app(
        meya, app_config=AppConfig.from_path(Path("."))
    )


def to_spec(element: Element, spec_type: Optional[Type[Spec]] = None):
    if not spec_type and isinstance(element, Component):
        spec_type = ComponentSpec
    elif not spec_type and isinstance(element, Trigger):
        spec_type = TriggerSpec
    elif not spec_type:
        spec_type = Spec
    return spec_type.from_element(element, test_type_registry)


def to_spec_dict(element: Element):
    return to_dict(to_spec(element))


async def verify_process_element(
    element: Element,
    sub_entry: Entry,
    expected_pub_entries: List[Entry],
    *,
    expected_db_requests: Optional[List[Tuple]] = None,
    expected_http_entries: Optional[List[HttpEntry]] = None,
    extra_elements: Optional[List[Element]] = None,
    log: Optional[LogView] = None,
    app_config: Optional[AppConfig] = None,
    thread: Optional[ThreadView] = None,
    user: Optional[UserView] = None,
    event_user: Optional[UserView] = None,
    http_mock: MockHttpView = None,
    time_to_freeze: Any = None,
):
    with ExitStack() as stack:
        sub_entry.parent_entry_ref = None
        sub_entry.trace_id = "-"
        db_view = MockDbView(expected_db_requests or [])
        stack.enter_context(DbView.current.set(db_view))
        stack.enter_context(Entry.current.set(sub_entry))
        stack.enter_context(
            Entry.current_encrypted.set(
                await db_view.encrypt_sensitive_entry(sub_entry)
            )
        )
        stack.enter_context(
            Entry.current_redacted.set(
                db_view.redact_sensitive_entry(sub_entry)
            )
        )
        if app_config is None:
            app_config = MagicMock()
        stack.enter_context(AppConfig.current.set(app_config))
        app_vault = MagicMock()
        stack.enter_context(AppVault.current.set(app_vault))
        element_processor = StaticElementProcessor()
        stack.enter_context(
            StaticElementProcessor.current.set(element_processor)
        )
        stack.enter_context(
            StaticElementProcessor.current_background_process_tasks.set(set())
        )
        source_registry = MagicMock()
        stack.enter_context(SourceRegistry.current.set(source_registry))
        assert type(element) not in test_type_registry.private
        if extra_elements is None:
            spec_registry = MagicMock()
        else:
            spec_registry = SpecRegistry(
                {
                    extra_element.id: to_spec(extra_element)
                    for extra_element in extra_elements
                },
                top_level_refs=[
                    Ref(extra_element.id) for extra_element in extra_elements
                ],
            )
            spec_registry.type_registry = test_type_registry
        stack.enter_context(SpecRegistry.current.set(spec_registry))
        stack.enter_context(TypeRegistry.current.set(test_type_registry))
        if http_mock:
            http_view = http_mock
        else:
            http_view = MockHttpView(
                db_view,
                expected_requests=[
                    item
                    for item in expected_http_entries or []
                    if isinstance(item, HttpRequestEntry)
                ],
                expected_responses=[
                    item
                    for item in expected_http_entries or []
                    if isinstance(item, HttpResponseEntry)
                ],
            )
        stack.enter_context(HttpView.current.set(http_view))
        if log is None:
            log = MockLogView()
        stack.enter_context(LogView.current.set(log))
        latency_stats = LatencyStats()
        stack.enter_context(LatencyStats.current.set(latency_stats))
        if thread is None:
            thread = create_thread(getattr(sub_entry, "thread_id", None))
        stack.enter_context(ThreadView.current.set(thread))
        if user is None:
            user = create_user()
        stack.enter_context(UserView.current.set(user))
        if isinstance(element, (Component, Trigger, Flow)):
            bot = next(
                (bot for bot in extra_elements or [] if isinstance(bot, Bot)),
                None,
            )
            if not bot:
                bot = create_bot(getattr(sub_entry, "bot_id", None))
            bot.thread = thread
            bot.user = user
            stack.enter_context(Bot.current.set(bot))
        else:
            bot = None
        if event_user is None:
            if isinstance(sub_entry, Event):
                event_user = create_user(sub_entry.user_id)
            elif isinstance(element, Component):
                event_user = bot.bot_user
            else:
                event_user = UserView()
        if bot:
            bot.event_user = event_user
        stack.enter_context(UserView.event_current.set(event_user))
        if time_to_freeze is None:
            time_to_freeze = from_utc_milliseconds_timestamp(
                frozen_milliseconds_timestamp
            )
        stack.enter_context(freeze_time(time_to_freeze))
        stack.enter_context(patch_uuid4_hex())
        stack.enter_context(patch_env())
        stack.enter_context(patch_private_env())
        spec = Spec.from_element(element)
        actual_pub_entries = await Element.process_from_spec(spec)
        actual_pub_entries += log.entries
        actual_pub_entries += thread.changes
        actual_pub_entries += user.changes
        actual_pub_entries += (
            event_user.changes if event_user is not user else []
        )
        for entry in expected_pub_entries + actual_pub_entries:
            entry.parent_entry_ref = None
            entry.trace_id = "-"
        if bot:
            extra_expected_pub_entries = []
            for entry in expected_pub_entries:
                bot.post_process(entry, extra_expected_pub_entries)
            expected_pub_entries.extend(extra_expected_pub_entries)
            extra_actual_pub_entries = []
            for entry in actual_pub_entries:
                bot.post_process(entry, extra_actual_pub_entries)
            actual_pub_entries.extend(extra_actual_pub_entries)
        await asyncio.gather(
            *StaticElementProcessor.current_background_process_tasks.get()
        )
    assert actual_pub_entries == expected_pub_entries
    assert [
        Entry.from_typed_dict(
            actual_pub_entry.to_typed_dict(test_type_registry),
            test_type_registry,
        )
        for actual_pub_entry in actual_pub_entries
    ] == actual_pub_entries
    assert len(db_view.expected_requests) == db_view.current_request


def generate_test_id(prefix: str):
    return f"{prefix}-{meya.util.uuid.uuid4_hex()}"


def create_log_message_entry(
    level: Level,
    message: str,
    *args: Any,
    scope: Scope = Scope.BOT,
    context: Optional[dict] = None,
    timestamp: int = frozen_milliseconds_timestamp,
) -> LogMessageEntry:
    return LogMessageEntry(
        args=list(args),
        context=context or {},
        level=level,
        message=message,
        scope=scope,
        timestamp=timestamp,
    )


def create_history_db_request(
    thread: ThreadView,
    end: str = "+",
    start: str = "-",
    count: int = 256,
    history_events: Optional[List[Event]] = None,
):
    return (
        "event",
        dict(thread_id=thread.id),
        end,
        start,
        count,
        history_events or [],
    )


def create_user_link_db_request(
    integration: Integration, integration_user_id: str, user: UserView
):
    return (
        [
            UserLinkEntry(
                integration_id=integration.id,
                integration_user_id=UserView._encode_integration_key_id(
                    integration_user_id
                ),
                user_id=user.id,
            )
        ],
    )


def create_thread_link_db_request(
    integration: Integration, integration_thread_id: str, thread: ThreadView
):
    return (
        [
            ThreadLinkEntry(
                integration_id=integration.id,
                integration_thread_id=ThreadView._encode_integration_key_id(
                    integration_thread_id
                ),
                thread_id=thread.id,
            )
        ],
    )


def create_user_unlink_db_request(
    integration: Integration, user: UserView, integration_user_id: str
):
    return (
        [
            UserUnlinkEntry(
                integration_id=integration.id,
                integration_user_id=UserView._encode_integration_key_id(
                    integration_user_id
                ),
                user_id=user.id,
            )
        ],
    )


def create_thread_unlink_db_request(
    integration: Integration, thread: ThreadView, integration_thread_id: str
):
    return (
        [
            ThreadUnlinkEntry(
                integration_id=integration.id,
                integration_thread_id=ThreadView._encode_integration_key_id(
                    integration_thread_id
                ),
                thread_id=thread.id,
            )
        ],
    )


def create_thread_data_db_request(thread: ThreadView):
    return "thread_data", dict(thread_id=thread.id), thread.data


def create_user_data_db_request(user: UserView):
    return "user_data", dict(user_id=user.id), user.data


def create_user_lookup_db_request(
    integration: Integration, integration_user_id: str, *users: UserView
):
    return (
        "user_lookup",
        dict(
            integration_id=integration.id,
            integration_user_id=UserView._encode_integration_key_id(
                integration_user_id
            ),
        ),
        [user.id for user in users],
    )


def create_thread_lookup_db_request(
    integration: Integration, integration_thread_id: str, *threads: ThreadView
):
    return (
        "thread_lookup",
        dict(
            integration_id=integration.id,
            integration_thread_id=ThreadView._encode_integration_key_id(
                integration_thread_id
            ),
        ),
        [thread.id for thread in threads],
    )


def create_user_reverse_lookup_db_request(
    integration: Integration, user: UserView, *integration_user_ids: str
):
    return (
        "user_reverse_lookup",
        dict(user_id=user.id, integration_id=integration.id),
        [
            UserView._encode_integration_key_id(integration_user_id)
            for integration_user_id in integration_user_ids
        ],
    )


def create_thread_reverse_lookup_db_request(
    integration: Integration, thread: ThreadView, *integration_thread_ids: str
):
    return (
        "thread_reverse_lookup",
        dict(thread_id=thread.id, integration_id=integration.id),
        [
            ThreadView._encode_integration_key_id(integration_thread_id)
            for integration_thread_id in integration_thread_ids
        ],
    )


def create_component_start_entry(
    component: Component,
    bot: Optional[Bot] = None,
    thread: Optional[ThreadView] = None,
    flow: Optional[str] = None,
    data: Optional[dict] = None,
    stack: Optional[List[StackFrame]] = None,
) -> ComponentStartEntry:
    return ComponentStartEntry(
        bot_id=bot.id if bot else generate_test_id("bot"),
        spec=to_spec_dict(component),
        data=data or {},
        flow=flow or generate_test_id("flow"),
        index=0,
        stack=stack or [],
        thread_id=thread
        and thread.id
        or (data or {}).get("event", {}).get("data", {}).get("thread_id")
        or generate_thread_id(),
    )


def create_component_next_entry(
    component_entry: ComponentEntry, data: Optional[dict] = None
) -> ComponentNextEntry:
    return ComponentNextEntry(
        bot_id=component_entry.bot_id,
        data={**component_entry.data, **(data or {})},
        flow=component_entry.flow,
        index=component_entry.index,
        spec=component_entry.spec,
        stack=component_entry.stack,
        thread_id=component_entry.thread_id,
    )


def create_flow_next_entry(
    bot_entry: Union[ComponentEntry, FlowStartEntry, FlowNextEntry],
    data: Optional[dict] = None,
) -> FlowNextEntry:
    return FlowNextEntry(
        bot_id=bot_entry.bot_id,
        data={**bot_entry.data, **(data or {})},
        flow=bot_entry.flow,
        index=bot_entry.index,
        stack=bot_entry.stack,
        thread_id=bot_entry.thread_id,
    )


def create_trigger_action_entry(bot_entry: BotEntry) -> TriggerActionEntry:
    bot_entry_dict = bot_entry.to_typed_dict(test_type_registry)
    return TriggerActionEntry(bot_entry_dict)


def create_mock_http_response(
    status: int, data: dict = None, text: str = None
) -> MockHttpView:
    return MockHttpView(
        expected_responses=[
            HttpResponseEntry(
                request_id=generate_test_id("request"),
                status=status,
                data=data,
                text=text,
                content_type=None,
                headers={},
            )
        ]
    )


def activate_triggers(
    component_entry: ComponentEntry, *triggers: Trigger
) -> List[TriggerActivateEntry]:
    return [
        TriggerActivateEntry(
            bot_id=component_entry.bot_id,
            spec=to_spec_dict(trigger),
            thread_id=component_entry.thread_id,
        )
        for trigger in triggers
    ]


def create_http_request_entry(
    integration: Integration,
    *,
    method: str = "POST",
    path: str = "",
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    host: str = "grid-test.meya.ai",
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
    content_type: str = "application/json",
    text: Optional[str] = None,
    app_id: str = "test_app",
    url: Optional[str] = None,
) -> HttpRequestEntry:
    return HttpRequestEntry(
        app_id=app_id,
        content_type=content_type,
        cookies=cookies or {},
        data=data,
        direction=Direction.RX,
        headers={
            "Content-Type": content_type,
            "Host": host,
            **(headers or {}),
        },
        integration_id=integration.id,
        integration_name=integration.NAME,
        method=method,
        params=params or {},
        request_id=generate_test_id("request"),
        text=text,
        url=url
        or f"https://{host}/gateway/v2/{integration.NAME}/{app_id}/{integration.id}{path}",
    )


def create_http_response_entry(
    request_entry: Optional[HttpRequestEntry] = None,
    *,
    status: int = 200,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> HttpResponseEntry:
    if data is None:
        data = dict(ok=True)
    return HttpResponseEntry(
        content_type="application/json",
        data=data,
        headers=headers or {},
        request_id=request_entry.request_id if request_entry else MISSING,
        status=status,
        text=None,
        url=request_entry.url if request_entry else None,
    )


def create_http_ws_upgrade_entry(
    request_entry: HttpRequestEntry, context: Optional[dict] = None
) -> HttpWsUpgradeEntry:
    return HttpWsUpgradeEntry(
        context=context or {}, request_id=request_entry.request_id
    )


def create_flow_start_entry(
    thread_id: Optional[str] = None,
    bot_id: Optional[str] = None,
    flow: Optional[str] = None,
    data: Optional[dict] = None,
) -> FlowStartEntry:
    return FlowStartEntry(
        bot_id=bot_id or generate_test_id("bot"),
        data=data
        or {generate_test_id("data-key"): generate_test_id("data-value")},
        flow=flow or generate_test_id("flow"),
        label=None,
        stack=[],
        thread_id=thread_id,
    )


def create_say_event(text: Optional[str]) -> SayEvent:
    return SayEvent(
        user_id=generate_user_id(), text=text, thread_id=generate_thread_id()
    )


def create_user(
    user_id: Optional[str] = None, data: Optional[dict] = None
) -> UserView:
    return UserView(id=user_id or generate_user_id(), data=data or {})


def create_thread(
    thread_id: Optional[str] = None, data: Optional[dict] = None
) -> ThreadView:
    return ThreadView(id=thread_id or generate_thread_id(), data=data or {})


def create_user_changes(user: UserView, new_data: dict) -> List[UserDataEntry]:
    new_user = UserView(id=user.id, data=to_dict(user.data))
    for key in new_data:
        new_user[key] = new_data[key]
    return new_user.changes


def create_thread_changes(
    thread: ThreadView, new_data: dict
) -> List[ThreadDataEntry]:
    new_thread = ThreadView(id=thread.id, data=to_dict(thread.data))
    for key in new_data:
        new_thread[key] = new_data[key]
    return new_thread.changes


def create_bot(bot_id: Optional[str] = None) -> Bot:
    bot = Bot(id=bot_id or generate_test_id("bot"))
    bot.bot_user = create_user(data=dict(type=UserType.BOT))
    return bot


async def verify_trigger_match(
    trigger: Trigger,
    event: Event,
    *,
    should_match: Optional[bool],
    confidence: Optional[Real] = None,
    original_confidence: Optional[Real] = None,
    match_data: dict = None,
    expected_db_requests: Optional[List[Tuple]] = None,
    http_mock: MockHttpView = None,
    log_entries: List[LogMessageEntry] = None,
    extra_elements: Optional[List[Element]] = None,
    event_user: Optional[UserView] = None,
):
    event.parent_entry_ref = None
    event.trace_id = "-"
    match_data = match_data or {}
    log_entries = log_entries or []
    trigger.action.entry["data"]["trace_id"] = "-"
    flow_start_entry = FlowStartEntry.from_typed_dict(
        trigger.action.entry, test_type_registry
    )
    flow_start_entry.data.update(
        {
            trigger.EVENT_KEY: event.to_typed_dict(test_type_registry),
            **match_data,
        }
    )
    if original_confidence is None:
        original_confidence = trigger.MAX_CONFIDENCE
    if confidence is not None:
        flow_start_entry.data.update(
            {
                trigger.CONFIDENCE_KEY: confidence,
                trigger.ORIGINAL_CONFIDENCE_KEY: original_confidence,
            }
        )
    else:
        flow_start_entry.data.update(
            {trigger.CONFIDENCE_KEY: original_confidence}
        )
    if should_match is True:
        match_result_entry = TriggerMatchEntry(
            bot_id=flow_start_entry.bot_id,
            thread_id=event.thread_id,
            action_entry=flow_start_entry.to_typed_dict(test_type_registry),
            confidence=flow_start_entry.data[trigger.CONFIDENCE_KEY],
        )
    elif should_match is False:
        match_result_entry = TriggerMatchEntry(
            bot_id=flow_start_entry.bot_id,
            thread_id=event.thread_id,
            action_entry=None,
            confidence=trigger.NO_CONFIDENCE,
        )
    else:
        match_result_entry = None
    await verify_process_element(
        element=trigger,
        sub_entry=event,
        expected_pub_entries=[
            *([match_result_entry] if match_result_entry else []),
            *log_entries,
        ],
        expected_db_requests=[]
        if expected_db_requests is None
        else expected_db_requests,
        http_mock=http_mock,
        extra_elements=[
            *(extra_elements or []),
            create_bot(flow_start_entry.bot_id),
        ],
        event_user=event_user,
    )
