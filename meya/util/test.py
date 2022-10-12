from pathlib import Path
from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "Use `unittest.mock.AsyncMock` instead of `meya.util.AsyncMock`",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class AsyncMockContextManager(AsyncMock):
    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "Use `unittest.mock.AsyncMock` instead of `meya.util.AsyncMockContextManager`",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)

    async def __aenter__(self, *args, **kwargs):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass


def is_root_cwd() -> bool:
    module_depth = len(__name__.split(".")) + 2
    root_path = Path(*Path(__file__).parts[:-module_depth])
    return root_path == Path.cwd()
