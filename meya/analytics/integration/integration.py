from dataclasses import dataclass
from meya.analytics.event.identify import IdentifyEvent
from meya.analytics.event.track import TrackEvent
from meya.bot.entry import BotEntry
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.entry import Entry
from meya.event.entry import Event
from meya.http.entry.request import HttpRequestEntry
from meya.integration.element import Integration
from meya.user.entry.data import UserDataEntry
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class AnalyticsIntegration(Integration):
    is_abstract: bool = meta_field(value=True)

    track_entries: bool = element_field(default=True)
    tracked_entries: List[str] = element_field(default_factory=list)
    untracked_entries: List[str] = element_field(default_factory=list)
    track_user_data: bool = element_field(default=True)
    tracked_user_data: List[str] = element_field(default_factory=list)
    untracked_user_data: List[str] = element_field(default_factory=list)
    entry: Union[Event, BotEntry, UserDataEntry] = process_field()
    redacted_entry: Union[Event, BotEntry, UserDataEntry] = process_field()

    async def accept_sensitive(self) -> bool:
        return await self.accept()

    def validate(self):
        super().validate()
        if self.tracked_entries and self.untracked_entries:
            raise self.validation_error(
                "only either tracked or untracked entries is supported"
            )
        if self.tracked_user_data and self.untracked_user_data:
            raise self.validation_error(
                "only either tracked or untracked user data is supported"
            )
        self.validate_entries(self.tracked_entries, "tracked")
        self.validate_entries(self.untracked_entries, "untracked")

    def validate_entries(self, entries, name):
        for entry in entries:
            entry_subclass = Entry.try_get_entry_type_subclass(entry)
            if not entry_subclass or not issubclass(
                entry_subclass, self.get_entry_type().__args__
            ):
                raise self.validation_error(f'invalid {name} entry "{entry}"')

    async def process(self) -> List[Entry]:
        entries = []
        if self.is_track:
            entries.append(await self.track())
        elif self.is_identify and self.entry_data:
            entries.append(await self.identify())
        return entries

    @property
    def is_track(self) -> bool:
        if (
            not isinstance(self.redacted_entry, (UserDataEntry, IdentifyEvent))
            and self.track_entries
        ):
            return self.is_entry_tracked
        else:
            return False

    @property
    def is_identify(self) -> bool:
        if (
            isinstance(self.redacted_entry, (UserDataEntry, IdentifyEvent))
            and self.track_user_data
        ):
            return self.is_entry_tracked
        else:
            return False

    @property
    def user_id(self) -> str:
        if self.is_identify:
            if isinstance(self.redacted_entry, IdentifyEvent):
                # special case
                return self.user.id
            else:
                return self.redacted_entry.user_id
        else:
            return self.user.id

    @property
    def entry_type(self) -> str:
        if isinstance(self.redacted_entry, TrackEvent):
            # special case
            return self.redacted_entry.event
        else:
            # simply use the entry_type
            return self.redacted_entry.get_entry_type()

    @property
    def entry_data(self) -> dict:
        if self.is_identify:
            if isinstance(self.redacted_entry, IdentifyEvent):
                # special case
                data = self.redacted_entry.data
            else:
                data = {self.redacted_entry.key: self.redacted_entry.value}
            # only track certain keys based on whitelist/blacklist
            return {
                key: data[key]
                for key in data
                if self._is_user_data_key_tracked(key)
            }
        else:
            if isinstance(self.redacted_entry, TrackEvent):
                # special case
                return self.redacted_entry.data
            else:
                return self.redacted_entry.to_dict()

    def _is_user_data_key_tracked(self, key: str) -> bool:
        if self.tracked_user_data:
            return key in set(self.tracked_user_data)
        else:
            return key not in set(self.untracked_user_data)

    @property
    def entry_context(self) -> Optional[Dict[str, Any]]:
        if isinstance(self.redacted_entry, Event):
            # special case
            return self.redacted_entry.context
        else:
            return None

    @property
    def entry_timestamp(self) -> float:
        if isinstance(self.redacted_entry, (TrackEvent, IdentifyEvent)):
            # special case
            return (
                self.redacted_entry.timestamp
                or self.redacted_entry.entry_posix_timestamp
            )
        else:
            return self.redacted_entry.entry_posix_timestamp

    @property
    def is_entry_tracked(self):
        if self.tracked_entries:
            result = self._is_entry_matched(self.tracked_entries)
        else:
            result = not self._is_entry_matched(self.untracked_entries)
        return result

    def _is_entry_matched(self, entry_type_list: List[str]) -> bool:
        return any(
            isinstance(
                self.redacted_entry, Entry.get_entry_type_subclass(entry_type)
            )
            for entry_type in entry_type_list
        )

    async def track(self) -> HttpRequestEntry:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")

    async def identify(self) -> HttpRequestEntry:
        """Must implement in subclass"""
        raise self.process_error("Not implemented")
