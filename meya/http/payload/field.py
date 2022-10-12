from dataclasses import MISSING
from dataclasses import field
from meya.util.dict import MISSING_FACTORY
from typing import Any
from typing import Callable
from typing import Optional


def payload_field(
    *,
    default: Any = MISSING,
    default_factory: Callable[[], Any] = MISSING,
    default_missing: bool = False,
    key: Optional[str] = None,
    repr: bool = True,
    sensitive: Any = MISSING,
    sensitive_factory: Callable[[], Any] = MISSING,
    **metadata,
):
    field_instance = None

    def _raise_missing():
        raise Exception(f'missing "{field_instance.name}" value')

    dict_default = default
    dict_default_factory = default_factory

    if default_missing:
        default = MISSING
        default_factory = MISSING_FACTORY
        if dict_default is MISSING and dict_default_factory is MISSING:
            dict_default_factory = MISSING_FACTORY

    if default is MISSING and default_factory is MISSING:
        # Our class hierarchy requires mixing default and non-default fields,
        # so treat everything as default but raise runtime errors
        default_factory = _raise_missing

    field_instance = field(
        init=True,
        default=default,
        default_factory=default_factory,
        metadata={
            **dict(
                dict_default=dict_default,
                dict_default_factory=dict_default_factory,
                key=key,
                sensitive=sensitive,
                sensitive_factory=sensitive_factory,
            ),
            **metadata,
        },
        repr=repr,
    )
    return field_instance
