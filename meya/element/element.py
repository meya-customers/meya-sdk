import asyncio

from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager
from contextlib import contextmanager
from dataclasses import Field
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from dataclasses import replace
from http import HTTPStatus
from meya.app_config import AppConfig
from meya.app_vault import AppVault
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.core.base_ref import BaseRef
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.core.source_location import SourceLocation
from meya.db.view.db import DbView
from meya.db.view.history import HistoryView
from meya.db.view.http import HttpView
from meya.db.view.log import LogView
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserView
from meya.element.element_error import ElementError
from meya.element.element_error import ElementImportError
from meya.element.element_error import ElementProcessError
from meya.element.element_error import ElementValidationError
from meya.element.field import context_field
from meya.element.field import element_field
from meya.element.field import process_field
from meya.entry import Entry
from meya.icon.spec import IconElementSpecUnion
from meya.util.context_var import ScopedContextVar
from meya.util.dict import MISSING_FACTORY
from meya.util.dict import dataclass_get_field
from meya.util.dict import dataclass_get_meta_value
from meya.util.dict import dataclass_get_own_meta_value
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from meya.util.latency.stats import LatencyStats
from traceback import print_exc
from typing import Any
from typing import Awaitable
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast


@dataclass
class Element:
    id: Optional[str] = element_field(
        default=None,
        help="Override the generated ID for this element",
        level=MetaLevel.HIDDEN,
    )
    source_location: Optional[SourceLocation] = element_field(
        default=None,
        help="Override the parsed source location for this element",
        level=MetaLevel.HIDDEN,
    )
    spec: Optional["Spec"] = context_field(
        default=None, help="Override the original spec for this element"
    )
    app_config: AppConfig = process_field()
    app_vault: AppVault = process_field()
    spec_registry: "AbstractSpecRegistry" = process_field()
    entry: Entry = process_field()
    encrypted_entry: Entry = process_field()
    redacted_entry: Entry = process_field()
    log: LogView = process_field()
    element_processor: "AbstractElementProcessor" = process_field()
    latency_stats: LatencyStats = process_field()
    db: DbView = process_field()
    thread: ThreadView = process_field()
    user: UserView = process_field()
    event_user: UserView = process_field()
    http: HttpView = process_field()
    history: HistoryView = process_field()

    def __post_init__(self):
        self.app_config = AppConfig.current.try_get()
        self.app_vault = AppVault.current.try_get()
        self.spec_registry = AbstractSpecRegistry.current.try_get()
        self.entry = Entry.current.try_get()
        self.encrypted_entry = Entry.current_encrypted.try_get()
        self.redacted_entry = Entry.current_redacted.try_get()
        self.log = LogView.current.try_get()
        self.element_processor = AbstractElementProcessor.current.try_get()
        self.latency_stats = LatencyStats.current.try_get()
        self.db = DbView.current.try_get()
        self.thread = ThreadView.current.try_get()
        self.user = UserView.current.try_get()
        self.event_user = UserView.event_current.try_get()
        self.http = HttpView.current.try_get()
        self.history = HistoryView()

    @classmethod
    def get_element_type(
        cls, type_registry: Optional[AbstractTypeRegistry] = None
    ) -> str:
        return (
            type_registry or AbstractTypeRegistry.current.get()
        ).reverse_alias[cls]

    @classmethod
    def get_entry_type(cls) -> type:
        return dataclass_get_field(cls, "entry").type

    @classmethod
    def get_extra_alias(cls) -> Optional[str]:
        return dataclass_get_own_meta_value(cls, "extra_alias")

    @classmethod
    def get_is_abstract(cls) -> bool:
        return dataclass_get_own_meta_value(cls, "is_abstract") or False

    @classmethod
    def get_meta_name(cls) -> Optional[str]:
        return dataclass_get_own_meta_value(cls, "meta_name")

    @classmethod
    def get_meta_icon(cls) -> IconElementSpecUnion:
        return (
            dataclass_get_meta_value(cls, "meta_icon")
            or "streamline-regular/05-internet-networks-servers/09-cloud/cloud-settings.svg"
        )

    @classmethod
    def get_meta_level(cls) -> Optional[float]:
        return dataclass_get_own_meta_value(cls, "meta_level")

    @classmethod
    def get_meta_group(cls) -> Optional[str]:
        return dataclass_get_meta_value(cls, "meta_group")

    @classmethod
    def get_meta_tags(cls) -> Optional[List[Type[MetaTag]]]:
        return dataclass_get_meta_value(cls, "meta_tags")

    @classmethod
    def get_run_in_app_container(cls) -> bool:
        return dataclass_get_meta_value(cls, "run_in_app_container") or False

    @classmethod
    def _get_field(cls, name: str) -> Optional[Field]:
        return next(
            (field for field in fields(cls) if field.name == name), None
        )

    def validate(self):
        pass

    @property
    def is_runtime(self) -> bool:
        return bool(self.entry)

    @property
    def is_design_time(self) -> bool:
        return not self.is_runtime

    def validation_error(self, message: str):
        return ElementValidationError(self.source_location, message)

    async def process(self) -> List[Entry]:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    def post_process_all(self, entries: List[Entry]) -> List[Entry]:
        extra_entries = []
        for entry in entries:
            self.post_process(entry, extra_entries)

        return entries + extra_entries

    def post_process(self, entry: Entry, extra_entries: List[Entry]) -> None:
        pass

    def process_error(self, message: str):
        return ElementProcessError(self.source_location, message)

    async def accept(self) -> bool:
        entry_type = self.get_entry_type()
        if getattr(entry_type, "__origin__", None) is Union:
            return isinstance(self.entry, entry_type.__args__)
        else:
            return isinstance(self.entry, entry_type)

    async def accept_sensitive(self) -> bool:
        return False

    @classmethod
    async def resolve(cls, ref: "Ref") -> Any:
        spec = cls.resolve_spec(ref)
        return await cls.render_from_spec(spec)

    @classmethod
    async def render_spec_data(cls, spec: "Spec") -> "Spec":
        return await AbstractElementProcessor.current.get().render_spec_data(
            spec
        )

    @classmethod
    async def render_from_spec(cls, spec: "Spec"):
        if spec.is_partial:
            spec = cls.resolve_spec(Ref(spec.id))
        if (
            spec.is_partial
            and spec.type in AbstractTypeRegistry.current.get().alias
        ):
            spec = await cls.render_spec_data(spec)
        return cls.from_spec(spec)

    @classmethod
    def from_spec(cls, spec: "Spec") -> "Element":
        assert spec.type is not None
        element_processor = AbstractElementProcessor.current.get()
        element = element_processor.create_proxy_element_for_spec(spec)
        if not element:
            type_registry = AbstractTypeRegistry.current.get()
            element_type = type_registry.alias.get(spec.type)
            if not element_type or not issubclass(element_type, Element):
                raise ElementImportError(
                    spec.source_location,
                    f'unable to find element type "{spec.type}"',
                )
            element_type = type_registry.private.get(
                element_type, element_type
            )
            assert spec.data is not None
            element = from_dict(
                element_type,
                {
                    "id": spec.id,
                    "source_location": spec.source_location,
                    "spec": spec,
                    **spec.data,
                },
            )
        return element

    @classmethod
    def resolve_spec(cls, ref: "Ref") -> "Spec":
        return AbstractSpecRegistry.current.get().resolve(ref)

    @classmethod
    def validate_from_spec(cls, spec: "Spec"):
        element = cls.from_spec(spec)
        element.validate()

    @classmethod
    async def process_from_ref(cls, ref: "Ref") -> List[Entry]:
        spec = cls.resolve_spec(ref)
        return await cls.process_from_spec(spec)

    @classmethod
    async def process_from_spec(cls, spec: "Spec") -> List[Entry]:
        pub_entries: List[Entry] = []
        async with cls._process_spec_log(spec.source_location, pub_entries):
            with cls._process_spec_thread_and_user() as change_entries:
                element = await cls.render_from_spec(spec)
                element.validate()

                # check if the entry is in scope for this element
                if element.entry.sensitive:
                    accept = await element.accept_sensitive()
                else:
                    accept = await element.accept()

                if accept:
                    # this is where the magic happens
                    entries = await element.process()
                    cls._process_spec_validate_entries(element, entries)
                    entries = element.post_process_all(entries)
                    pub_entries.extend(entries)
        return change_entries + pub_entries

    @classmethod
    @asynccontextmanager
    async def _process_spec_log(
        cls, source_location: SourceLocation, pub_entries: List[Entry]
    ):
        from meya.http.entry.request import HttpRequestEntry
        from meya.http.entry.response import HttpResponseEntry
        from meya.log.entry.exception import LogExceptionEntry

        log = replace(LogView.current.get(), source_location=source_location)
        with LogView.current.set(log):
            try:
                yield
            except Exception as e:
                entry = Entry.current_redacted.get()
                if isinstance(entry, LogExceptionEntry):
                    print("Exception processing exception log", entry)
                    print_exc()
                elif isinstance(e, ElementError):
                    log.error(str(e))
                else:
                    # TODO: differentiate between developer and system exceptions?
                    log.exception()
                root_entry = await DbView.current.get().root_entry(entry)
                if isinstance(root_entry, HttpRequestEntry):
                    pub_entries.append(
                        HttpResponseEntry(
                            request_id=root_entry.request_id,
                            content_type="application/json",
                            data=dict(
                                ok=False,
                                reason=(
                                    "An app error occurred. Please view your "
                                    "app logs for more information."
                                ),
                            ),
                            text=None,
                            status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            url=root_entry.url,
                        )
                    )

    @classmethod
    @contextmanager
    def _process_spec_thread_and_user(cls):
        change_entries: List[Entry] = []
        old_thread = ThreadView.current.get()
        new_thread = ThreadView(id=old_thread.id, data=old_thread.data)
        old_user = UserView.current.get()
        new_user = UserView(id=old_user.id, data=old_user.data)
        old_event_user = UserView.event_current.get()
        new_event_user = UserView(
            id=old_event_user.id, data=old_event_user.data
        )
        with ThreadView.current.set(new_thread):
            with UserView.current.set(new_user):
                with UserView.event_current.set(new_event_user):
                    yield change_entries
                    if new_thread.id == old_thread.id:
                        old_thread.update(new_thread.data)
                    else:
                        change_entries.extend(new_thread.changes)
                    if new_user.id == old_user.id:
                        old_user.update(new_user.data)
                    else:
                        change_entries.extend(new_user.changes)
                    if new_event_user is not new_user:
                        if new_event_user.id == old_event_user.id:
                            old_event_user.update(new_event_user.data)
                        else:
                            change_entries.extend(new_event_user.changes)

    @classmethod
    def _process_spec_validate_entries(
        cls, element: "Element", entries: Any
    ) -> None:
        if not isinstance(entries, list):
            raise ElementProcessError(
                element.source_location,
                f"{type(element).__name__}.process() did not return a list of entries: {entries}",
            )

        for entry in entries:
            if not isinstance(entry, Entry):
                raise ElementProcessError(
                    element.source_location,
                    f"{type(element).__name__}.process() returned a non-entry: {entry}",
                )

    @staticmethod
    async def gather_all_entries(
        tasks: Iterable[Awaitable[List[Entry]]],
    ) -> List[Entry]:
        all_entries = await asyncio.gather(*tasks)
        return [entry for entries in all_entries for entry in entries]


@dataclass
class Spec:
    type: Optional[str]
    data: Optional[Dict[str, Any]]
    id: Optional[str]
    source_location: Optional[SourceLocation]
    timeout: Optional[int] = None
    parent_flow_id: Optional[str] = None
    element_type: ClassVar[Type[Element]] = Element
    trigger_when: Any = field(default_factory=MISSING_FACTORY)

    @property
    def is_partial(self):
        if self.data is None:
            assert self.id is not None
            return True
        else:
            return False

    @classmethod
    def from_element(
        cls,
        element: Element,
        type_registry: Optional[AbstractTypeRegistry] = None,
    ) -> "Spec":
        assert isinstance(element, cls.element_type)
        data = to_dict(element)
        element_id = data.pop("id", None)
        source_location = data.pop("source_location", None)
        data.pop("spec", None)
        return cls(
            type=element.get_element_type(type_registry),
            data=data,
            id=element_id,
            source_location=source_location,
        )


@dataclass
class Ref(BaseRef):
    element_type: ClassVar[Type[Element]] = Element

    def validate(self, source_location: Optional[SourceLocation]):
        spec = AbstractSpecRegistry.current.get().try_resolve(self)
        if not spec:
            raise ElementValidationError(
                source_location,
                f'unresolved {self.element_type.__name__} reference "{self}"',
            )

        element_type = AbstractTypeRegistry.current.get().alias.get(
            spec.type, None
        )
        if not element_type:
            # Proxy element type, no type check possible
            # TODO Try using type registry subclass info
            return

        if not issubclass(element_type, self.element_type):
            raise ElementValidationError(
                source_location,
                f'"{self}" reference is a {element_type.__name__}'
                f" not a {self.element_type.__name__}",
            )


AnyRef = TypeVar("AnyRef", bound=Ref)


@dataclass
class AbstractSpecRegistry(ABC):
    current: ClassVar = cast(
        ScopedContextVar["AbstractSpecRegistry"],
        ScopedContextVar("spec_registry"),
    )

    @abstractmethod
    def resolve(self, ref: Ref) -> Spec:
        pass

    @abstractmethod
    def try_resolve(self, ref: Ref) -> Optional[Spec]:
        pass

    @abstractmethod
    def find_top_level_refs(self, ref_type: Type[AnyRef]) -> List[AnyRef]:
        pass


@dataclass
class AbstractElementProcessor(ABC):
    current: ClassVar = cast(
        ScopedContextVar["AbstractElementProcessor"],
        ScopedContextVar("element_processor"),
    )
    current_background_process_tasks: ClassVar = cast(
        ScopedContextVar[Set[asyncio.Task]],
        ScopedContextVar("background_process_tasks"),
    )

    def create_proxy_element_for_spec(self, spec: Spec) -> Optional[Element]:
        return None

    @abstractmethod
    async def render_spec_data(self, spec: Spec) -> Spec:
        pass


class StaticElementProcessor(AbstractElementProcessor):
    async def render_spec_data(
        self, spec: Spec
    ) -> Tuple[Dict[str, Any], List[Entry]]:
        raise NotImplementedError()
