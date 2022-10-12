from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from meya.db.view.thread import ThreadView
from meya.db.view.user import UserView
from typing import Any
from typing import ClassVar
from typing import Dict


class CollectionScope(Enum):
    USER = "user"
    USER_OVERWRITE = "user_overwrite"
    THREAD = "thread"
    THREAD_OVERWRITE = "thread_overwrite"
    EVENT = "event"


@dataclass
class DataCollector:
    collect_config: InitVar[dataclass]
    user_view: UserView
    thread_view: ThreadView

    def __post_init__(self, collect_config: dataclass):
        self._custom_context = {}
        self._event_context = {}
        self._collect_config = collect_config

    def __setattr__(self, key, value):
        if not hasattr(self, "_collect_config"):
            super().__setattr__(key, value)
            return
        if not hasattr(self._collect_config, key):
            raise ValueError(
                f"No scope defined for '{key}' in your collect config."
            )
        scope = getattr(self._collect_config, key)
        if scope is None:
            return
        elif scope == CollectionScope.EVENT:
            if key == "context" and isinstance(value, dict):
                self._custom_context.update(value)
            else:
                self._event_context[key] = value
        elif scope == CollectionScope.USER:
            if self.user_view[key] is None:
                self.user_view[key] = value
        elif scope == CollectionScope.USER_OVERWRITE:
            self.user_view[key] = value
        elif scope == CollectionScope.THREAD:
            if self.thread_view[key] is None:
                self.thread_view[key] = value
        elif scope == CollectionScope.THREAD_OVERWRITE:
            self.thread_view[key] = value
        else:
            raise ValueError(f"Unknown scope '{scope}' for key '{key}'")

    @property
    def event_context(self):
        return {**self._custom_context, **self._event_context}


@dataclass
class LanguageData:
    DEFAULT_SCOPE: ClassVar = CollectionScope.USER


@dataclass
class IpAddressData:
    DEFAULT_SCOPE: ClassVar = CollectionScope.EVENT


@dataclass
class ReferrerData:
    DEFAULT_SCOPE: ClassVar = CollectionScope.EVENT


@dataclass
class UrlData:
    DEFAULT_SCOPE: ClassVar = CollectionScope.EVENT


@dataclass
class ContextData:
    DEFAULT_SCOPE: ClassVar = CollectionScope.EVENT
