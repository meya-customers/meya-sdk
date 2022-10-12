from jinja2 import contextfilter
from jinja2.runtime import Context
from meya.db.view.db import DbView
from meya.sensitive_data import REDACTED_TEXT
from meya.sensitive_data import SensitiveDataRef
from meya.time.timedelta import to_timedelta
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Any
from typing import Dict
from typing import Optional


@contextfilter
async def encrypt_sensitive_filter(
    ctx: Context, value: Any, ttl: Optional[str] = None
) -> Dict[str, Any]:
    db_view: DbView = ctx["db"]
    if ttl is not None:
        ttl = to_timedelta(ttl)
    ref = await db_view.encrypt_sensitive(value, ttl)
    return to_dict(ref)


@contextfilter
async def decrypt_sensitive_filter(ctx: Context, value: Dict[str, Any]) -> Any:
    db_view: DbView = ctx["db"]
    ref = from_dict(SensitiveDataRef, value)
    if not isinstance(ref, SensitiveDataRef):
        raise ValueError()
    return await db_view.decrypt_sensitive(ref)


@contextfilter
async def try_decrypt_sensitive_filter(
    ctx: Context, value: Dict[str, Any], default: Any = REDACTED_TEXT
) -> Any:
    db_view: DbView = ctx["db"]
    try:
        ref = from_dict(SensitiveDataRef, value)
        if not isinstance(ref, SensitiveDataRef):
            raise ValueError()
        return await db_view.try_decrypt_sensitive(ref, default)
    except ValueError:
        return value


async def redact_sensitive_filter(
    value: Dict[str, Any], default: Any = REDACTED_TEXT
) -> Any:
    try:
        ref = from_dict(SensitiveDataRef, value)
        if not isinstance(ref, SensitiveDataRef):
            raise ValueError()
        return default
    except ValueError:
        return value
