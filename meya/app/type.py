from meya.util.enum import SimpleEnum
from meya.util.enum import SimpleEnumMeta
from meya.util.text.case import snake_case_to_human
from typing import Optional
from typing import Union


class AppType(str, SimpleEnum, metaclass=SimpleEnumMeta):
    DEV = "DEV"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    def __str__(self):
        return str(self.value)

    def to_human(self) -> str:
        return snake_case_to_human(self.value)

    @classmethod
    def choices(cls):
        return [
            (member.value, snake_case_to_human(member.value)) for member in cls
        ]

    @staticmethod
    def from_str(app_type: Union[str, "AppType"]) -> Optional["AppType"]:
        try:
            return AppType(app_type)
        except ValueError:
            return None

    @staticmethod
    def is_dev(app_type: str) -> bool:
        return AppType.from_str(app_type) == AppType.DEV

    @staticmethod
    def is_staging(app_type: str) -> bool:
        return AppType.from_str(app_type) == AppType.STAGING

    @staticmethod
    def is_production(app_type: str) -> bool:
        return AppType.from_str(app_type) == AppType.PRODUCTION
