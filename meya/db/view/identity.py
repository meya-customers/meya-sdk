from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from meya.db.view.db import DbView
from meya.entry import Entry
from meya.util.dict import to_dict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from urllib.parse import quote
from urllib.parse import unquote

AnyEntry = TypeVar("AnyEntry", bound=Entry)


@dataclass
class IdentityView(ABC):
    id: Optional[str] = field(default=None)
    data: Dict[str, Any] = field(default_factory=dict)
    _original_data: Dict[str, Any] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._reset_original_data()

    def clear(self) -> None:
        """
        Remove all keys and values.
        """
        for key in self.data:
            self.data[key] = None

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update with keys and values from data.
        """
        for key in data:
            self.data[key] = data[key]

    def update_default(self, data: Dict[str, Any]) -> None:
        """
        Update with keys and values from data if not set on self.
        """
        for key in data:
            if self.data.get(key) is None:
                self.data[key] = data[key]

    def __getattr__(self, key: str) -> Any:
        if key.startswith("_"):
            raise AttributeError(
                f"type object '{type(self).__name__}' cannot get attribute '{key}'"
            )
        else:
            return self[key]

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in ("id", "data", "_original_data"):
            super().__setattr__(key, value)
        elif hasattr(type(self), key) or key.startswith("_"):
            raise AttributeError(
                f"type object '{type(self).__name__}' cannot set attribute '{key}'"
            )
        else:
            self[key] = value

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    async def _identify(
        self,
        integration_key_id: str,
        integration_id: str,
        data: Optional[Dict[str, Any]],
        default_data: Optional[Dict[str, Any]],
        key_id: str,
        link_entry: Entry,
    ) -> None:
        assert integration_key_id
        existing_key_ids = await self._query_lookup_view(
            integration_id, integration_key_id
        )
        if existing_key_ids:
            key_id = existing_key_ids[0]
        else:
            await DbView.current.get().publish(link_entry)
        await self._load(key_id)
        if data:
            self.update(data)
        if default_data:
            self.update_default(default_data)

    async def _link(
        self,
        integration_key_id: str,
        integration_id: str,
        link_entry: Entry,
        make_unlink_entry: Callable[[str], Entry],
    ) -> None:
        assert self.id
        assert integration_key_id
        existing_integration_key_ids = await self._reverse_lookup_multi(
            integration_id
        )
        unlink_entries = [
            make_unlink_entry(existing_integration_key_id)
            for existing_integration_key_id in existing_integration_key_ids
            if existing_integration_key_id != integration_key_id
        ]
        link_entries = (
            []
            if integration_key_id in existing_integration_key_ids
            else [link_entry]
        )
        await DbView.current.get().publish(
            *unlink_entries, *link_entries, preclaim_after_publish_all=True
        )

    async def _link_multi(self, link_entry: Entry) -> None:
        assert self.id
        await DbView.current.get().publish(link_entry)

    async def _unlink(
        self,
        integration_key_id: Optional[str],
        integration_id: str,
        make_unlink_entry: Callable[[str], Entry],
    ) -> None:
        assert self.id
        if integration_key_id:
            unlink_integration_key_ids = [integration_key_id]
        else:
            unlink_integration_key_ids = await self._reverse_lookup_multi(
                integration_id
            )
        unlink_entries = [
            make_unlink_entry(unlink_integration_key_id)
            for unlink_integration_key_id in unlink_integration_key_ids
        ]
        await DbView.current.get().publish(
            *unlink_entries, preclaim_after_publish_all=True
        )

    @classmethod
    async def _lookup(
        cls, integration_key_id: str, integration_id: str
    ) -> Optional[str]:
        existing_key_id = await cls._try_lookup(
            integration_key_id, integration_id
        )
        assert existing_key_id, f"Lookup failed for {integration_key_id}"
        return existing_key_id

    @classmethod
    async def _try_lookup(
        cls, integration_key_id: str, integration_id: str
    ) -> Optional[str]:
        existing_key_ids = await cls._lookup_multi(
            integration_key_id, integration_id
        )
        if existing_key_ids:
            return existing_key_ids[0]
        else:
            return None

    @classmethod
    async def _lookup_multi(
        cls, integration_key_id: str, integration_id: str
    ) -> List[str]:
        return await cls._query_lookup_view(integration_id, integration_key_id)

    async def _reverse_lookup(self, integration_id: str) -> Optional[str]:
        existing_integration_key_id = await self._try_reverse_lookup(
            integration_id
        )
        assert (
            existing_integration_key_id
        ), f"Reverse lookup failed for {self.id}"
        return existing_integration_key_id

    async def _try_reverse_lookup(self, integration_id: str) -> Optional[str]:
        existing_integration_key_ids = await self._reverse_lookup_multi(
            integration_id
        )
        if existing_integration_key_ids:
            return existing_integration_key_ids[0]
        else:
            return None

    async def _reverse_lookup_multi(self, integration_id: str) -> List[str]:
        assert self.id
        return await self._query_reverse_lookup_view(self.id, integration_id)

    async def _load(self, key_id: str, *, find_loaded: bool = True) -> None:
        assert key_id
        found_loaded = (
            next(
                (
                    loaded
                    for loaded in self._find_loaded()
                    if loaded and loaded.id == key_id
                ),
                None,
            )
            if find_loaded
            else None
        )
        if found_loaded:
            data = found_loaded.data
            original_data = found_loaded._original_data
        else:
            data = await self._query_data_view(key_id)
            original_data = None
        self.id = key_id
        self.data = data
        if original_data:
            self._original_data = original_data
        else:
            self._reset_original_data()

    @classmethod
    @abstractmethod
    async def _query_data_view(cls, key_id: str) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    async def _query_lookup_view(
        cls, integration_id: str, integration_key_id: str
    ) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    async def _query_reverse_lookup_view(
        cls, key_id: str, integration_id: str
    ) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def _find_loaded(cls) -> List[Optional["IdentityView"]]:
        pass

    def _reset_original_data(self) -> None:
        # Copy original data to avoid modifying it
        self._original_data = to_dict(self.data)

    def _changes(
        self, make_data_entry: Callable[[str, Any], AnyEntry]
    ) -> List[AnyEntry]:
        if not self.id:
            return []
        results = []
        for key in sorted(self.data.keys()):
            value = self.data[key]
            if value != self._original_data.get(key):
                results.append(make_data_entry(key, value))
        return results

    @staticmethod
    def _integration_id(integration_id: Optional[str]) -> str:
        if integration_id:
            return integration_id
        else:
            from meya.integration.element import Integration

            return Integration.current.get().id

    @staticmethod
    def _encode_integration_key_id(integration_key_id: str) -> str:
        return quote(integration_key_id)

    @staticmethod
    def _decode_integration_key_id(integration_key_id: str) -> str:
        return unquote(integration_key_id)
