from contextlib import contextmanager
from time import perf_counter
from typing import Callable
from typing import Optional
from typing import Union


@contextmanager
def perf_measure(
    task: Union[str, Callable[[], str]], limit: Optional[float] = None
):
    perf_start = perf_counter()
    try:
        yield
    finally:
        perf_duration = perf_counter() - perf_start
        if limit is None or perf_duration > limit:
            if not isinstance(task, str):
                task = task()
            print(f"{task} in {perf_duration:.3f}s")
