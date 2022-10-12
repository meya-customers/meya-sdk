from dataclasses import dataclass
from meya.db.view.db import DbView
from meya.db.view.identity import IdentityView
from meya.event.entry import Event
from meya.user.entry.data import UserDataEntry
from meya.user.entry.link import UserLinkEntry
from meya.user.entry.unlink import UserUnlinkEntry
from meya.util.context_var import ScopedContextVar
from meya.util.generate_id import generate_user_id
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import cast


class UserType(str):
    def __new__(cls, value: Optional[str] = None, **kwargs):
        if value is None:
            value = "user"
        return super().__new__(cls, value, **kwargs)

    def __getattr__(self, item):
        return item == self


UserType.AGENT = UserType("agent")
UserType.BOT = UserType("bot")
UserType.SYSTEM = UserType("system")
UserType.USER = UserType()


@dataclass
class UserView(IdentityView):
    current: ClassVar = cast(ScopedContextVar["UserView"], ScopedContextVar())
    event_current: ClassVar = cast(
        ScopedContextVar["UserView"], ScopedContextVar("event")
    )

    def __getitem__(self, key: str):
        if key == "type":
            return UserType(super().__getitem__(key))
        else:
            return super().__getitem__(key)

    async def identify(
        self,
        integration_user_id: str,
        *,
        integration_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        default_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Find and load the Meya user linked to from an integration user. If not
        linked yet, create a new Meya user. If data provided, merge into loaded
        user data. If default data provided, merge into loaded user data for
        keys not yet set.
        """
        integration_user_id = self._encode_integration_key_id(
            integration_user_id
        )
        integration_id = self._integration_id(integration_id)
        user_id = generate_user_id()
        await self._identify(
            integration_user_id,
            integration_id,
            data,
            default_data,
            user_id,
            UserLinkEntry(
                integration_id=integration_id,
                integration_user_id=integration_user_id,
                user_id=user_id,
            ),
        )

    async def link(
        self, integration_user_id: str, *, integration_id: Optional[str] = None
    ) -> None:
        """
        Link the current Meya user to an integration user, allowing only this
        single link.
        """
        integration_user_id = self._encode_integration_key_id(
            integration_user_id
        )
        integration_id = self._integration_id(integration_id)
        await self._link(
            integration_user_id,
            integration_id,
            UserLinkEntry(
                integration_id=integration_id,
                integration_user_id=integration_user_id,
                user_id=self.id,
            ),
            lambda unlink_integration_user_id: UserUnlinkEntry(
                integration_id=integration_id,
                integration_user_id=unlink_integration_user_id,
                user_id=self.id,
            ),
        )

    async def link_multi(
        self, integration_user_id: str, *, integration_id: Optional[str] = None
    ) -> None:
        """
        Link the current Meya user to an integration user, allowing multiple
        links.
        """
        integration_user_id = self._encode_integration_key_id(
            integration_user_id
        )
        integration_id = self._integration_id(integration_id)
        return await self._link_multi(
            UserLinkEntry(
                integration_id=integration_id,
                integration_user_id=integration_user_id,
                user_id=self.id,
            )
        )

    async def unlink(
        self,
        integration_user_id: Optional[str] = None,
        *,
        integration_id: Optional[str] = None,
    ) -> None:
        """
        Unlink the current Meya user from an integration user.
        """
        integration_user_id = (
            integration_user_id
            and self._encode_integration_key_id(integration_user_id)
        )
        integration_id = self._integration_id(integration_id)
        await self._unlink(
            integration_user_id,
            integration_id,
            lambda unlink_integration_user_id: UserUnlinkEntry(
                integration_id=integration_id,
                integration_user_id=unlink_integration_user_id,
                user_id=self.id,
            ),
        )

    @classmethod
    async def lookup(
        cls, integration_user_id: str, *, integration_id: Optional[str] = None
    ) -> str:
        """
        Find the user ID linked to an integration user.
        """
        integration_user_id = cls._encode_integration_key_id(
            integration_user_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._lookup(integration_user_id, integration_id)

    @classmethod
    async def try_lookup(
        cls, integration_user_id: str, *, integration_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Try to find the user ID linked to an integration user.
        """
        integration_user_id = cls._encode_integration_key_id(
            integration_user_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._try_lookup(integration_user_id, integration_id)

    @classmethod
    async def lookup_multi(
        cls, integration_user_id: str, *, integration_id: Optional[str] = None
    ) -> List[str]:
        """
        Find all user IDs linked to an integration user.
        """
        integration_user_id = cls._encode_integration_key_id(
            integration_user_id
        )
        integration_id = cls._integration_id(integration_id)
        return await cls._lookup_multi(integration_user_id, integration_id)

    async def reverse_lookup(
        self, *, integration_id: Optional[str] = None
    ) -> str:
        """
        Find the integration user ID linked to the current user.
        """
        integration_id = self._integration_id(integration_id)
        integration_user_id = await self._reverse_lookup(integration_id)
        return self._decode_integration_key_id(integration_user_id)

    async def try_reverse_lookup(
        self, *, integration_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Try to find the integration user ID linked to the current user.
        """
        integration_id = self._integration_id(integration_id)
        integration_user_id = await self._try_reverse_lookup(integration_id)
        return integration_user_id and self._decode_integration_key_id(
            integration_user_id
        )

    async def reverse_lookup_multi(
        self, *, integration_id: Optional[str] = None
    ) -> List[str]:
        """
        Find all integration user IDs linked to the current user.
        """
        integration_id = self._integration_id(integration_id)
        integration_user_ids = await self._reverse_lookup_multi(integration_id)
        return [
            self._decode_integration_key_id(integration_user_id)
            for integration_user_id in integration_user_ids
        ]

    async def load(self, user_id: str, *, find_loaded: bool = True) -> None:
        """
        Load data for a specific user.
        """
        await self._load(user_id, find_loaded=find_loaded)

    @classmethod
    async def get(
        cls, user_id: str, *, find_loaded: bool = True
    ) -> "UserView":
        """
        Get and load a new instance of a specific user.
        """
        user = cls()
        await user.load(user_id, find_loaded=find_loaded)
        return user

    @classmethod
    async def get_event_user(
        cls, event: Event, *, find_loaded: bool = True
    ) -> "UserView":
        """
        Get and load a new instance of a specific event's user.
        """
        return await cls.get(event.user_id, find_loaded=find_loaded)

    @classmethod
    async def get_event_users(
        cls, events: List[Event], *, find_loaded: bool = True
    ) -> Dict[str, "UserView"]:
        event_user_ids = set(event.user_id for event in events)
        return {
            event_user_id: await cls.get(
                event_user_id, find_loaded=find_loaded
            )
            for event_user_id in event_user_ids
        }

    @property
    def changes(self) -> List[UserDataEntry]:
        return self._changes(
            lambda key, value: UserDataEntry(
                key=key, user_id=self.id, value=value
            )
        )

    @classmethod
    async def _query_data_view(cls, key_id: str) -> Dict[str, Any]:
        return await DbView.current.get().query_user_data_view(key_id)

    @classmethod
    async def _query_lookup_view(
        cls, integration_id: str, integration_key_id: str
    ) -> List[str]:
        return await DbView.current.get().query_user_lookup_view(
            integration_id, integration_key_id
        )

    @classmethod
    async def _query_reverse_lookup_view(
        cls, key_id: str, integration_id: str
    ) -> List[str]:
        return await DbView.current.get().query_user_reverse_lookup_view(
            key_id, integration_id
        )

    @classmethod
    def _find_loaded(cls) -> List[Optional["UserView"]]:
        from meya.bot.element import Bot

        bot = Bot.current.try_get()
        return [
            cls.current.try_get(),
            cls.event_current.try_get(),
            bot.bot_user if bot else None,
        ]
