from dataclasses import MISSING
from dataclasses import field
from meya.util.dict import MISSING_FACTORY
from typing import Any
from typing import Callable
from typing import Optional


def response_field(
    *,
    default: Any = MISSING,
    sensitive: Any = MISSING,
    sensitive_factory: Callable[[], Any] = MISSING,
    **metadata,
):
    if default is MISSING:
        default_factory = MISSING_FACTORY
    else:
        default_factory = MISSING
    return field(
        default=default,
        default_factory=default_factory,
        metadata={
            **dict(sensitive=sensitive, sensitive_factory=sensitive_factory),
            **metadata,
        },
    )


def meta_field(*, value: Any = None):
    return field(
        init=False,
        default=None,
        repr=False,
        compare=False,
        metadata=dict(value=value),
    )


def element_field(
    *,
    signature: bool = False,
    default: Any = MISSING,
    default_factory: Callable[[], Any] = MISSING,
    snippet_default: Optional[str] = None,
    repr: bool = True,
    help: Optional[str] = None,
    meta_name: Optional[str] = None,
    level: Optional[float] = None,
    **metadata,
):
    field_instance = None

    def _raise_missing():
        raise Exception(f'missing "{field_instance.name}" value')

    dict_default = default
    dict_default_factory = default_factory

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
                snippet_default=snippet_default,
                signature=signature,
                from_context=False,
                dict_default=dict_default,
                dict_default_factory=dict_default_factory,
                help=help,
                meta_name=meta_name,
                level=level,
            ),
            **metadata,
        },
        repr=repr,
    )
    return field_instance


def context_field(
    default: Any = MISSING,
    default_factory: Callable[[], Any] = MISSING,
    help: Optional[str] = None,
):
    field_instance = None

    def _raise_missing():
        raise Exception(f'missing "{field_instance.name}" value')

    if default is MISSING and default_factory is MISSING:
        # Our class hierarchy requires mixing default and non-default fields,
        # so treat everything as default but raise runtime errors
        default_factory = _raise_missing

    field_instance = field(
        init=True,
        default=default,
        default_factory=default_factory,
        metadata=dict(
            signature=False, from_context=True, default_missing=True, help=help
        ),
    )
    return field_instance


def process_field(*, default: Any = None):
    return field(init=False, default=default, compare=False, repr=False)
