from meya.util.enum import SimpleEnum
from meya.util.enum import SimpleEnumMeta
from meya.util.text.case import snake_case_to_human
from typing import Optional
from typing import Union


class AppState(str, SimpleEnum, metaclass=SimpleEnumMeta):
    DELETED = "DELETED"
    DEPLOYING = "DEPLOYING"
    ERROR = "ERROR"
    RUNNING = "RUNNING"
    STARTING = "STARTING"
    STOPPED = "STOPPED"

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
    def from_str(state: Union[str, "AppState"]) -> Optional["AppState"]:
        try:
            return AppState(state)
        except ValueError:
            return None

    @staticmethod
    def is_deleted(state: str) -> bool:
        return AppState.from_str(state) == AppState.DELETED

    @staticmethod
    def is_deploying(state: str) -> bool:
        return AppState.from_str(state) == AppState.DEPLOYING

    @staticmethod
    def is_error(state: str) -> bool:
        return AppState.from_str(state) == AppState.ERROR

    @staticmethod
    def is_running(state: str) -> bool:
        return AppState.from_str(state) == AppState.RUNNING

    @staticmethod
    def is_starting(state: str) -> bool:
        return AppState.from_str(state) == AppState.STARTING

    @staticmethod
    def is_stopped(state: str) -> bool:
        return AppState.from_str(state) == AppState.STOPPED
