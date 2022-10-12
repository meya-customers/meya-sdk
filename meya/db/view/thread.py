from dataclasses import dataclass
from meya.db.view.db import DbView
from meya.db.view.identity import IdentityView
from meya.thread.entry.data import ThreadDataEntry
from meya.thread.entry.link import ThreadLinkEntry
from meya.thread.entry.unlink import ThreadUnlinkEntry
from meya.util.context_var import ScopedContextVar
from meya.util.generate_id import generate_thread_id
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import cast


class ThreadMode(str):
    def __new__(cls, value: Optional[str] = None, **kwargs):
        if value is None:
            value = "bot"
        return super().__new__(cls, value, **kwargs)

    def __getattr__(self, item):
        return item == self


ThreadMode.AGENT = ThreadMode("agent")
ThreadMode.BOT = ThreadMode()


@dataclass
class ThreadView(IdentityView):
    current: ClassVar = cast(
        ScopedContextVar["ThreadView"], ScopedContextVar()
    )

    def __getitem__(self, key: str):
        if key == "mode":
            return ThreadMode(super().__getitem__(key))
        else:
            return super().__getitem__(key)

    async def identify(
        self,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        default_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Find and load the Meya thread linked to from an integration thread. If
        not linked yet, create a new Meya thread. If data provided, merge into
        loaded thread data. If default data provided, merge into loaded thread
        data for keys not yet set.
        """
        integration_thread_id = self._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = self._integration_id(integration_id)
        thread_id = generate_thread_id()
        await self._identify(
            integration_thread_id,
            integration_id,
            data,
            default_data,
            thread_id,
            ThreadLinkEntry(
                integration_id=integration_id,
                integration_thread_id=integration_thread_id,
                thread_id=thread_id,
            ),
        )

    async def link(
        self,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
    ) -> None:
        """
        Link the current Meya thread to an integration thread, allowing only
        this single link.
        """
        integration_thread_id = self._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = self._integration_id(integration_id)
        await self._link(
            integration_thread_id,
            integration_id,
            ThreadLinkEntry(
                integration_id=integration_id,
                integration_thread_id=integration_thread_id,
                thread_id=self.id,
            ),
            lambda unlink_integration_thread_id: ThreadUnlinkEntry(
                integration_id=integration_id,
                integration_thread_id=unlink_integration_thread_id,
                thread_id=self.id,
            ),
        )

    async def link_multi(
        self,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
    ) -> None:
        """
        Link the current Meya thread to an integration thread, allowing multiple
        links.
        """
        integration_thread_id = self._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = self._integration_id(integration_id)
        return await self._link_multi(
            ThreadLinkEntry(
                integration_id=integration_id,
                integration_thread_id=integration_thread_id,
                thread_id=self.id,
            )
        )

    async def unlink(
        self,
        integration_thread_id: Optional[str] = None,
        *,
        integration_id: Optional[str] = None,
    ) -> None:
        """
        Unlink the current Meya thread from an integration thread.
        """
        integration_thread_id = (
            integration_thread_id
            and self._encode_integration_key_id(integration_thread_id)
        )
        integration_id = self._integration_id(integration_id)
        await self._unlink(
            integration_thread_id,
            integration_id,
            lambda unlink_integration_thread_id: ThreadUnlinkEntry(
                integration_id=integration_id,
                integration_thread_id=unlink_integration_thread_id,
                thread_id=self.id,
            ),
        )

    @classmethod
    async def lookup(
        cls,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
    ) -> str:
        """
        Find the thread ID linked to an integration thread.
        """
        integration_thread_id = cls._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._lookup(integration_thread_id, integration_id)

    @classmethod
    async def try_lookup(
        cls,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Try to find the thread ID linked to an integration thread.
        """
        integration_thread_id = cls._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._try_lookup(integration_thread_id, integration_id)

    @classmethod
    async def lookup_multi(
        cls,
        integration_thread_id: str,
        *,
        integration_id: Optional[str] = None,
    ) -> List[str]:
        """
        Find all thread IDs linked to an integration thread.
        """
        integration_thread_id = cls._encode_integration_key_id(
            integration_thread_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._lookup_multi(integration_thread_id, integration_id)

    async def reverse_lookup(
        self, *, integration_id: Optional[str] = None
    ) -> str:
        """
        Find the integration thread ID linked to the current thread.
        """
        integration_id = self._integration_id(integration_id)
        integration_thread_id = await self._reverse_lookup(integration_id)
        return self._decode_integration_key_id(integration_thread_id)

    async def try_reverse_lookup(
        self, *, integration_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Try to find the integration thread ID linked to the current thread.
        """
        integration_id = self._integration_id(integration_id)
        integration_thread_id = await self._try_reverse_lookup(integration_id)
        return integration_thread_id and self._decode_integration_key_id(
            integration_thread_id
        )

    async def reverse_lookup_multi(
        self, *, integration_id: Optional[str] = None
    ) -> List[str]:
        """
        Find all integration thread IDs linked to the current thread.
        """
        integration_id = self._integration_id(integration_id)
        integration_thread_ids = await self._reverse_lookup_multi(
            integration_id
        )
        return [
            self._decode_integration_key_id(integration_thread_id)
            for integration_thread_id in integration_thread_ids
        ]

    async def load(self, thread_id: str, *, find_loaded: bool = True) -> None:
        """
        Load data for a specific thread.
        """
        await self._load(thread_id, find_loaded=find_loaded)

    @classmethod
    async def get(
        cls, thread_id: str, *, find_loaded: bool = True
    ) -> "ThreadView":
        """
        Get and load a new instance of a specific thread.
        """
        thread = cls()
        await thread.load(thread_id, find_loaded=find_loaded)
        return thread

    @property
    def changes(self) -> List[ThreadDataEntry]:
        return self._changes(
            lambda key, value: ThreadDataEntry(
                key=key, thread_id=self.id, value=value
            )
        )

    @classmethod
    async def _query_data_view(cls, key_id: str) -> Dict[str, Any]:
        return await DbView.current.get().query_thread_data_view(key_id)

    @classmethod
    async def _query_lookup_view(
        cls, integration_id: str, integration_key_id: str
    ) -> List[str]:
        return await DbView.current.get().query_thread_lookup_view(
            integration_id, integration_key_id
        )

    @classmethod
    async def _query_reverse_lookup_view(
        cls, key_id: str, integration_id: str
    ) -> List[str]:
        return await DbView.current.get().query_thread_reverse_lookup_view(
            key_id, integration_id
        )

    @classmethod
    def _find_loaded(cls) -> List[Optional["ThreadView"]]:
        return [cls.current.try_get()]
