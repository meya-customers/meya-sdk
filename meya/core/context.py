from meya.app_config import AppConfig
from meya.app_vault import AppVault
from meya.bot.element import Bot
from meya.component.entry import ComponentEntry
from meya.db.view.db import DbView
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserView
from meya.entry import Entry
from meya.event.entry import Event
from meya.flow.entry import FlowEntry
from meya.sensitive_data import REDACTED_TEXT
from meya.sensitive_data import SensitiveDataRef
from meya.sensitive_data.template import decrypt_sensitive_filter
from meya.sensitive_data.template import encrypt_sensitive_filter
from meya.sensitive_data.template import redact_sensitive_filter
from meya.sensitive_data.template import try_decrypt_sensitive_filter
from meya.util.dict import from_dict
from meya.util.template import environment_async
from meya.util.undefined import MISSING_UNDEFINED
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple


def create_load_context() -> Dict[str, Any]:
    return dict(
        bot=MISSING_UNDEFINED,
        config=AppConfig.current.get(),
        vault=AppVault.current.get(),
        entry=MISSING_UNDEFINED,
        encrypted_entry=MISSING_UNDEFINED,
        redacted_entry=MISSING_UNDEFINED,
        event=MISSING_UNDEFINED,
        event_user=MISSING_UNDEFINED,
        encrypted_event_user=MISSING_UNDEFINED,
        redacted_event_user=MISSING_UNDEFINED,
        flow=MISSING_UNDEFINED,
        encrypted_flow=MISSING_UNDEFINED,
        redacted_flow=MISSING_UNDEFINED,
        thread=MISSING_UNDEFINED,
        encrypted_thread=MISSING_UNDEFINED,
        redacted_thread=MISSING_UNDEFINED,
        user=MISSING_UNDEFINED,
        encrypted_user=MISSING_UNDEFINED,
        redacted_user=MISSING_UNDEFINED,
        db=MISSING_UNDEFINED,
    )


async def create_render_context() -> Dict[str, Any]:
    thread, encrypted_thread, redacted_thread = _get_thread_scope(
        ThreadView.current.get()
    )
    user, encrypted_user, redacted_user = _get_user_scope(
        UserView.current.get()
    )
    event_user, encrypted_event_user, redacted_event_user = _get_user_scope(
        UserView.event_current.get()
    )
    entry, encrypted_entry, redacted_entry, event = _get_entry()
    flow, encrypted_flow, redacted_flow = _get_flow_scope()
    return dict(
        bot=Bot.current.try_get(),
        config=AppConfig.current.get(),
        entry=entry,
        encrypted_entry=encrypted_entry,
        redacted_entry=redacted_entry,
        event=event,
        event_user=event_user,
        encrypted_event_user=encrypted_event_user,
        redacted_event_user=redacted_event_user,
        flow=flow,
        encrypted_flow=encrypted_flow,
        redacted_flow=redacted_flow,
        thread=thread,
        encrypted_thread=encrypted_thread,
        redacted_thread=redacted_thread,
        user=user,
        encrypted_user=encrypted_user,
        redacted_user=redacted_user,
        vault=AppVault.current.get(),
        db=DbView.current.get(),
    )


environment_async.filters["encrypt_sensitive"] = encrypt_sensitive_filter
environment_async.filters["decrypt_sensitive"] = decrypt_sensitive_filter
environment_async.filters[
    "try_decrypt_sensitive"
] = try_decrypt_sensitive_filter
environment_async.filters["redact_sensitive"] = redact_sensitive_filter


class FlowScope(dict):
    def __getitem__(self, key):
        return _try_decrypt_sensitive_value(super().__getitem__(key))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class EncryptedFlowScope(dict):
    pass


class RedactedFlowScope(dict):
    def __getitem__(self, key):
        return _redact_sensitive_value(super().__getitem__(key))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class ThreadScope(ThreadView):
    def __getitem__(self, key):
        return _try_decrypt_sensitive_value(super().__getitem__(key))


class EncryptedThreadScope(ThreadView):
    pass


class RedactedThreadScope(ThreadView):
    def __getitem__(self, key):
        return _redact_sensitive_value(super().__getitem__(key))


class UserScope(UserView):
    def __getitem__(self, key):
        return _try_decrypt_sensitive_value(super().__getitem__(key))


class EncryptedUserScope(UserView):
    pass


class RedactedUserScope(UserView):
    def __getitem__(self, key):
        return _redact_sensitive_value(super().__getitem__(key))


def _try_decrypt_sensitive_value(value: Any) -> Any:
    if isinstance(value, dict):
        try:
            ref = from_dict(SensitiveDataRef, value)
            db_view = DbView.current.get()
            return db_view.try_decrypt_sensitive(ref)
        except ValueError:
            return value
    else:
        return value


def _redact_sensitive_value(value: Any) -> Any:
    if isinstance(value, dict):
        try:
            from_dict(SensitiveDataRef, value)
            return REDACTED_TEXT
        except ValueError:
            return value
    else:
        return value


def _get_entry() -> Tuple[
    Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]
]:
    entry = Entry.current.get()
    entry_dict = entry.to_typed_dict()
    encrypted_entry_dict = Entry.current_encrypted.get().to_typed_dict()
    redacted_entry_dict = Entry.current_redacted.get().to_typed_dict()
    return (
        entry_dict,
        encrypted_entry_dict,
        redacted_entry_dict,
        (entry_dict if isinstance(entry, Event) else None),
    )


def _get_flow_scope() -> Tuple[
    Optional[FlowScope],
    Optional[EncryptedFlowScope],
    Optional[RedactedFlowScope],
]:
    entry = Entry.current.get()
    if isinstance(entry, (FlowEntry, ComponentEntry)):
        return (
            FlowScope(entry.data),
            EncryptedFlowScope(entry.data),
            RedactedFlowScope(entry.data),
        )
    else:
        return None, None, None


def _get_thread_scope(
    thread: ThreadView,
) -> Tuple[ThreadScope, EncryptedThreadScope, RedactedThreadScope]:
    return (
        ThreadScope(id=thread.id, data=thread.data),
        EncryptedThreadScope(id=thread.id, data=thread.data),
        RedactedThreadScope(id=thread.id, data=thread.data),
    )


def _get_user_scope(
    user: UserView,
) -> Tuple[UserScope, EncryptedUserScope, RedactedUserScope]:
    return (
        UserScope(id=user.id, data=user.data),
        EncryptedUserScope(id=user.id, data=user.data),
        RedactedUserScope(id=user.id, data=user.data),
    )
