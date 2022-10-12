import inspect

from contextlib import AbstractContextManager
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import TypeVar

T = TypeVar("T")


class SimpleContextVar(Generic[T]):
    def __init__(self, variant: str = ""):
        caller_module_name = inspect.stack()[1].frame.f_globals["__name__"]
        self.var = ContextVar(
            "/".join(filter(None, [caller_module_name, variant])), default=None
        )

    def get(self) -> T:
        current = self.try_get()
        assert current is not None, f"{self.var.name} context var not set"
        return current

    def try_get(self) -> Optional[T]:
        return self.var.get()

    def set(self, new: T) -> AbstractContextManager:
        token = self.var.set(new)

        @contextmanager
        def scope():
            try:
                yield
            finally:
                self.var.reset(token)

        return scope()


class ScopedContextVar(Generic[T]):
    def __init__(self, variant: str = ""):
        caller_module_name = inspect.stack()[1].frame.f_globals["__name__"]
        self.var = ContextVar(
            "/".join(filter(None, [caller_module_name, variant])), default=None
        )

    def get(self) -> T:
        current: Optional[ScopedContextVarState[T]] = self.var.get()
        assert current is not None, f"{self.var.name} context var not set"
        return current.get()

    def try_get(self) -> Optional[T]:
        state: Optional[ScopedContextVarState[T]] = self.var.get()
        return state and state.try_get()

    @contextmanager
    def set(self, new: T) -> None:
        with ScopedContextVarState.set(self.var, new) as new_state:
            token = self.var.set(new_state)
            try:
                yield
            finally:
                self.var.reset(token)


@dataclass
class ScopedContextVarState(Generic[T]):
    var: ContextVar
    value: Optional[T]

    def get(self) -> T:
        current = self.value
        assert current is not None, f"{self.var.name} context var out of scope"
        return current

    def try_get(self) -> Optional[T]:
        return self.value

    @classmethod
    @contextmanager
    def set(cls, var: ContextVar, new_value: T) -> "ScopedContextVar[T]":
        state = cls(var, new_value)
        try:
            yield state
        finally:
            state.value = None
