import pytz

from dataclasses import dataclass
from datetime import datetime
from meya.component.element import Component
from meya.core.meta_level import MetaLevel
from meya.core.meta_tag import MetaTag
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.time.meta_tag import TimeTag
from meya.time.time import Timezone
from meya.time.time import utcnow
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type


@dataclass
class AgentAvailabilityDataResponse:
    ok: bool = response_field()


@dataclass
class TimeAvailabilityComponent(Component):
    meta_level: float = meta_field(value=MetaLevel.INTERMEDIATE)
    meta_tags: List[Type[MetaTag]] = meta_field(value=[TimeTag])

    timezone: Timezone = element_field(default=Timezone.AMERICA_TORONTO)
    # 9-12,13-16:30
    mon: Optional[str] = element_field(default=None)
    tue: Optional[str] = element_field(default=None)
    wed: Optional[str] = element_field(default=None)
    thu: Optional[str] = element_field(default=None)
    fri: Optional[str] = element_field(default=None)
    sat: Optional[str] = element_field(default=None)
    sun: Optional[str] = element_field(default=None)

    @property
    def schedule(self):
        return {
            "mon": self.mon,
            "tue": self.tue,
            "wed": self.wed,
            "thu": self.thu,
            "fri": self.fri,
            "sat": self.sat,
            "sun": self.sun,
        }

    @property
    def tz(self):
        return pytz.timezone(self.timezone.value)

    def validate(self):
        super().validate()
        tz = self.tz
        day = None
        try:
            now = utcnow().replace(tzinfo=pytz.utc)
            for day, slots in self.schedule.items():
                self.get_time_slots(now, slots, tz)
        except pytz.UnknownTimeZoneError as e:
            raise self.validation_error(f"Unknown timezone {e}")
        except ValueError as e:
            raise self.validation_error(
                f'Incorrect schedule format for "{day}": {e}'
            )

    async def start(self) -> List[Entry]:
        return self.respond(
            data=AgentAvailabilityDataResponse(
                ok=self.check_availability(self.schedule, self.tz)
            )
        )

    def check_availability(self, schedule: Dict[str, str], tz) -> bool:
        now = utcnow().replace(tzinfo=pytz.utc)
        slots = list(schedule.values())
        for t_from, t_to in self.get_time_slots(now, slots[now.weekday()], tz):
            if t_from < now < t_to:
                return True
        return False

    @staticmethod
    def get_time_slots(
        now: datetime, slots: str, tz
    ) -> List[Tuple[datetime, datetime]]:
        s = []
        if not slots:
            s.append((now, now))
            return s

        for slot in slots.split(","):
            t_from, t_to = [
                pytz.utc.normalize(
                    tz.localize(
                        datetime.strptime(
                            t if ":" in t else t + ":00", "%H:%M"
                        ).replace(day=now.day, month=now.month, year=now.year)
                    )
                )
                for t in slot.strip().split("-")
            ]
            if t_to < t_from:
                raise ValueError(
                    f'"{tz.normalize(t_from).strftime("%H:%M")}" must be earlier '
                    f'than "{tz.normalize(t_to).strftime("%H:%M")}"'
                )
            s.append((t_from, t_to))
        return s
