from abc import ABC
from abc import abstractmethod
from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import replace
from datetime import timedelta
from meya.bot.entry import BotEntry
from meya.entry import Entry
from meya.event.entry import Event
from meya.http.entry import HttpEntry
from meya.log.entry import LogEntry
from meya.presence.event import PresenceEvent
from meya.sensitive_data import REDACTED_TEXT
from meya.sensitive_data import SensitiveDataRef
from meya.thread.entry import ThreadEntry
from meya.user.entry import UserEntry
from meya.util.context_var import ScopedContextVar
from meya.util.dict import dataclass_field_default
from meya.util.dict import dataclass_field_sensitive
from meya.util.dict import dataclass_init_fields
from meya.util.dict import from_dict
from meya.util.dict import is_data_class
from meya.util.dict import to_dict
from meya.ws.entry import WsEntry
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import cast

T = TypeVar("T")
TEntry = TypeVar("TEntry", bound=Entry)


@dataclass
class DbQueueConfig:
    cache_maxlen: int


@dataclass
class DbLedgerConfig:
    cache_maxlen: int
    cache_ttl: timedelta
    sensitive_ttl: Optional[timedelta]
    persist: bool


@dataclass
class DbHashViewConfig:
    cache_ttl: timedelta
    persist: bool


@dataclass
class DbSetViewConfig:
    cache_ttl: timedelta
    persist: bool


@dataclass
class DbBlobConfig:
    sensitive_ttl: Optional[timedelta]


@dataclass
class DbConfig:
    bot_queue: DbQueueConfig
    bot_ledger: DbLedgerConfig
    bot_active_triggers_view: DbSetViewConfig
    event_queue: DbQueueConfig
    event_ledger: DbLedgerConfig
    http_queue: DbQueueConfig
    http_ledger: DbLedgerConfig
    log_queue: DbQueueConfig
    log_ledger: DbLedgerConfig
    presence_queue: DbQueueConfig
    presence_ledger: DbLedgerConfig
    presence_device_view: DbHashViewConfig
    thread_queue: DbQueueConfig
    thread_ledger: DbLedgerConfig
    thread_data_view: DbHashViewConfig
    thread_lookup_view: DbSetViewConfig
    thread_reverse_lookup_view: DbSetViewConfig
    user_queue: DbQueueConfig
    user_ledger: DbLedgerConfig
    user_data_view: DbHashViewConfig
    user_lookup_view: DbSetViewConfig
    user_reverse_lookup_view: DbSetViewConfig
    ws_queue: DbQueueConfig
    ws_ledger: DbLedgerConfig
    blob: DbBlobConfig

    def __getitem__(self, item: str):
        return getattr(self, item)

    def get_queue(self, queue: str) -> DbQueueConfig:
        return self[f"{queue}_queue"]

    def get_ledger(self, ledger: str) -> DbLedgerConfig:
        return self[f"{ledger}_ledger"]

    def get_hash_view(self, hash_view: str) -> DbHashViewConfig:
        return self[f"{hash_view}_hash_view"]

    def get_set_view(self, set_view: str) -> DbSetViewConfig:
        return self[f"{set_view}_set_view"]


@dataclass
class DbView(ABC):
    current: ClassVar = cast(ScopedContextVar["DbView"], ScopedContextVar())

    @property
    @abstractmethod
    def config(self) -> Optional[DbConfig]:
        pass

    @abstractmethod
    async def publish(
        self, *entries: Entry, preclaim_after_publish_all: bool = False
    ) -> None:
        pass

    async def query_bot_ledger(
        self,
        bot_id: str,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[BotEntry]:
        return await self._query_ledger(
            "bot",
            dict(bot_id=bot_id, thread_id=thread_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_event_ledger(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[Event]:
        return await self._query_ledger(
            "event",
            dict(thread_id=thread_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_http_ledger(
        self,
        request_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[HttpEntry]:
        return await self._query_ledger(
            "http",
            dict(request_id=request_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_log_ledger(
        self,
        trace_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[LogEntry]:
        return await self._query_ledger(
            "log", dict(trace_id=trace_id), end, start, count, include_internal
        )

    async def query_presence_ledger(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[PresenceEvent]:
        return await self._query_ledger(
            "presence",
            dict(thread_id=thread_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_thread_ledger(
        self,
        thread_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[ThreadEntry]:
        return await self._query_ledger(
            "thread",
            dict(thread_id=thread_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_user_ledger(
        self,
        user_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[UserEntry]:
        return await self._query_ledger(
            "user", dict(user_id=user_id), end, start, count, include_internal
        )

    async def query_ws_ledger(
        self,
        request_id: str,
        end: str = "+",
        start: str = "-",
        count: int = 256,
        include_internal: bool = False,
    ) -> List[WsEntry]:
        return await self._query_ledger(
            "ws",
            dict(request_id=request_id),
            end,
            start,
            count,
            include_internal,
        )

    async def query_bot_active_triggers_view(
        self, bot_id: str, thread_id: str
    ) -> List[Dict[str, Any]]:
        return await self._query_set_view(
            "bot_active_triggers", dict(bot_id=bot_id, thread_id=thread_id)
        )

    async def query_presence_device_view(
        self, user_id: str, device_id: str
    ) -> Dict[str, Any]:
        return await self._query_hash_view(
            "presence_device", dict(user_id=user_id, device_id=device_id)
        )

    async def query_thread_data_view(self, thread_id: str) -> Dict[str, Any]:
        return await self._query_hash_view(
            "thread_data", dict(thread_id=thread_id)
        )

    async def query_thread_lookup_view(
        self, integration_id: str, integration_thread_id: str
    ) -> List[str]:
        return await self._query_set_view(
            "thread_lookup",
            dict(
                integration_id=integration_id,
                integration_thread_id=integration_thread_id,
            ),
        )

    async def query_thread_reverse_lookup_view(
        self, thread_id: str, integration_id: str
    ) -> List[str]:
        return await self._query_set_view(
            "thread_reverse_lookup",
            dict(thread_id=thread_id, integration_id=integration_id),
        )

    async def query_user_data_view(self, user_id: str) -> Dict[str, Any]:
        return await self._query_hash_view("user_data", dict(user_id=user_id))

    async def query_user_lookup_view(
        self, integration_id: str, integration_user_id: str
    ) -> List[str]:
        return await self._query_set_view(
            "user_lookup",
            dict(
                integration_id=integration_id,
                integration_user_id=integration_user_id,
            ),
        )

    async def query_user_reverse_lookup_view(
        self, user_id: str, integration_id: str
    ) -> List[str]:
        return await self._query_set_view(
            "user_reverse_lookup",
            dict(user_id=user_id, integration_id=integration_id),
        )

    @abstractmethod
    async def encrypt_sensitive(
        self, sensitive_obj: Any, ttl: Optional[timedelta] = None
    ) -> SensitiveDataRef:
        pass

    async def encrypt_sensitive_fields(
        self,
        sensitive_obj: T,
        ttl: Optional[timedelta] = None,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> T:
        # TODO Recurse into lists, dicts, etc.
        init_fields = is_data_class(
            type(sensitive_obj)
        ) and dataclass_init_fields(type(sensitive_obj))
        if not init_fields:
            return sensitive_obj

        encrypted_fields = {}
        for init_field in init_fields:
            key = init_field.name
            value = getattr(sensitive_obj, key)
            default, default_factory = dataclass_field_default(init_field)
            sensitive, sensitive_factory = dataclass_field_sensitive(
                init_field
            )
            if value is MISSING or isinstance(value, SensitiveDataRef):
                pass
            elif sensitive is not MISSING or sensitive_factory is not MISSING:
                if default is not MISSING:
                    default_value = default
                elif default_factory is not MISSING:
                    default_value = default_factory()
                else:
                    default_value = MISSING
                if value != default_value:
                    # Encrypt any non-default sensitive field value
                    encrypted_value = await self.encrypt_sensitive(
                        to_dict(
                            value,
                            preserve_nones=preserve_nones,
                            to_camel_case_fields=to_camel_case_fields,
                        ),
                        ttl,
                    )
                    encrypted_fields[key] = encrypted_value
            else:
                encrypted_value = await self.encrypt_sensitive_fields(
                    value, ttl
                )
                if encrypted_value is not value:
                    encrypted_fields[key] = encrypted_value

        if encrypted_fields:
            return replace(sensitive_obj, **encrypted_fields)
        else:
            return sensitive_obj

    async def encrypt_sensitive_entry(
        self, sensitive_entry: TEntry, ttl: Optional[timedelta] = None
    ) -> TEntry:
        if not ttl:
            ttl = self.config.get_ledger(
                sensitive_entry.get_entry_ledger()
            ).sensitive_ttl

        if sensitive_entry.sensitive:
            encrypted_entry = await self.encrypt_sensitive_fields(
                sensitive_entry, ttl
            )
            encrypted_entry.entry_id = sensitive_entry.entry_id
            return encrypted_entry
        else:
            return sensitive_entry

    @abstractmethod
    async def decrypt_sensitive(self, ref: SensitiveDataRef) -> Any:
        pass

    @abstractmethod
    async def root_entry(self, entry: Entry) -> Entry:
        pass

    async def try_decrypt_sensitive(
        self, ref: SensitiveDataRef, default: Any = REDACTED_TEXT
    ) -> Any:
        try:
            return await self.decrypt_sensitive(ref)
        except ValueError:
            return default

    async def try_decrypt_sensitive_fields(self, sensitive_obj: T) -> T:
        # TODO Recurse into lists, dicts, etc.
        init_fields = is_data_class(
            type(sensitive_obj)
        ) and dataclass_init_fields(type(sensitive_obj))
        if not init_fields:
            return sensitive_obj

        decrypted_fields = {}
        for init_field in init_fields:
            key = init_field.name
            value = getattr(sensitive_obj, key)
            sensitive, sensitive_factory = dataclass_field_sensitive(
                init_field
            )
            if (
                sensitive is not MISSING or sensitive_factory is not MISSING
            ) and isinstance(value, SensitiveDataRef):
                decrypted_value = await self.try_decrypt_sensitive(
                    value, MISSING
                )
                if decrypted_value is MISSING:
                    if sensitive is not MISSING:
                        decrypted_value = sensitive
                    else:
                        decrypted_value = sensitive_factory()
                decrypted_fields[key] = from_dict(
                    init_field.type, decrypted_value
                )
            else:
                decrypted_value = await self.try_decrypt_sensitive_fields(
                    value
                )
                if decrypted_value is not value:
                    decrypted_fields[key] = decrypted_value

        if decrypted_fields:
            return replace(sensitive_obj, **decrypted_fields)
        else:
            return sensitive_obj

    async def try_decrypt_sensitive_entry(
        self, sensitive_entry: TEntry
    ) -> TEntry:
        if sensitive_entry.sensitive:
            decrypted_entry = await self.try_decrypt_sensitive_fields(
                sensitive_entry
            )
            decrypted_entry.entry_id = sensitive_entry.entry_id
            return decrypted_entry
        else:
            return sensitive_entry

    def redact_sensitive_fields(self, sensitive_obj: T) -> T:
        # TODO Recurse into lists, dicts, etc.
        init_fields = is_data_class(
            type(sensitive_obj)
        ) and dataclass_init_fields(type(sensitive_obj))
        if not init_fields:
            return sensitive_obj

        redacted_fields = {}
        for init_field in init_fields:
            key = init_field.name
            value = getattr(sensitive_obj, key)
            default, default_factory = dataclass_field_default(init_field)
            sensitive, sensitive_factory = dataclass_field_sensitive(
                init_field
            )

            if default is not MISSING:
                default_value = default
            elif default_factory is not MISSING:
                default_value = default_factory()
            else:
                default_value = MISSING

            if value is MISSING or value == default_value:
                sensitive = MISSING
                sensitive_factory = MISSING

            if sensitive is not MISSING:
                redacted_fields[key] = sensitive
            elif sensitive_factory is not MISSING:
                redacted_value = sensitive_factory()
                redacted_fields[key] = redacted_value
            else:
                redacted_value = self.redact_sensitive_fields(value)
                if redacted_value is not value:
                    redacted_fields[key] = redacted_value

        if redacted_fields:
            return replace(sensitive_obj, **redacted_fields)
        else:
            return sensitive_obj

    def redact_sensitive_entry(self, sensitive_entry: TEntry) -> TEntry:
        if sensitive_entry.sensitive:
            redacted_entry = self.redact_sensitive_fields(sensitive_entry)
            redacted_entry.entry_id = sensitive_entry.entry_id
            return redacted_entry
        else:
            return sensitive_entry

    @abstractmethod
    async def _query_hash_view(
        self, view: str, instance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def _query_ledger(
        self,
        ledger: str,
        instance_data: Dict[str, Any],
        end: str,
        start: str,
        count: int,
        include_internal: bool = False,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def _query_set_view(
        self, view: str, instance_data: Dict[str, Any]
    ) -> List[Any]:
        pass
