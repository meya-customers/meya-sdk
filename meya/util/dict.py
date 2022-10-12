from dataclasses import MISSING
from dataclasses import Field
from dataclasses import fields
from datetime import timedelta
from enum import Enum
from functools import lru_cache
from math import isinf
from math import isnan
from meya.sensitive_data import REDACTED_TEXT
from meya.sensitive_data import SensitiveDataRef
from meya.time.timedelta import from_timedelta
from meya.time.timedelta import to_timedelta
from meya.util.camel_case import to_camel_case
from meya.util.form_data import BinaryFile
from numbers import Real
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_type_hints

MISSING_FACTORY = lambda: MISSING
NONE_FACTORY = lambda: None


@lru_cache(maxsize=None)
def dataclass_fields(data_class_type: type) -> Optional[List[Field]]:
    try:
        # noinspection PyDataclass
        results = list(fields(data_class_type))
        hints = get_type_hints(data_class_type)
        for result in results:
            result.type = hints[result.name]
        return results
    except TypeError:
        return None


def dataclass_get_field(data_class_type: type, name: str) -> Optional[Field]:
    return next(
        (
            field
            for field in dataclass_fields(data_class_type) or []
            if field.name == name
        ),
        None,
    )


@lru_cache(maxsize=None)
def dataclass_init_fields(data_class_type: type) -> Optional[List[Field]]:
    all_fields = dataclass_fields(data_class_type)
    if all_fields is None:
        return None
    else:
        return [field for field in all_fields if field.init]


def dataclass_get_init_field(
    data_class_type: type, name: str
) -> Optional[Field]:
    return next(
        (
            field
            for field in dataclass_init_fields(data_class_type) or []
            if field.name == name
        ),
        None,
    )


@lru_cache(maxsize=None)
def dataclass_meta_fields(data_class_type: type) -> Optional[List[Field]]:
    all_fields = dataclass_fields(data_class_type)
    if all_fields is None:
        return None
    else:
        return [
            field
            for field in all_fields
            if not field.init and "value" in field.metadata
        ]


def dataclass_get_meta_field(
    data_class_type: type, name: str
) -> Optional[Field]:
    return next(
        (
            field
            for field in dataclass_meta_fields(data_class_type) or []
            if field.name == name
        ),
        None,
    )


def dataclass_get_meta_value(data_class_type: type, name: str) -> Any:
    meta_field = dataclass_get_meta_field(data_class_type, name)
    if not meta_field:
        return None
    else:
        return meta_field.metadata["value"]


def dataclass_get_own_meta_value(data_class_type: type, name: str) -> Any:
    meta_field = dataclass_get_meta_field(data_class_type, name)
    if not meta_field:
        return None
    else:
        base_meta_fields = [
            dataclass_get_meta_field(base, name)
            for base in data_class_type.__bases__
        ]
        for base_field in base_meta_fields:
            if meta_field is base_field:
                return None

        return meta_field.metadata["value"]


@lru_cache(maxsize=None)
def is_data_class(data_class_type: type) -> bool:
    return dataclass_init_fields(data_class_type) is not None


@lru_cache(maxsize=None)
def dataclass_field_default(field: Field) -> Tuple[Any, Any]:
    if "dict_default" in field.metadata:
        default = field.metadata["dict_default"]
    else:
        default = field.default
    if "dict_default_factory" in field.metadata:
        default_factory = field.metadata["dict_default_factory"]
    else:
        default_factory = field.default_factory
    return default, default_factory


@lru_cache(maxsize=None)
def dataclass_field_snippet_default(field: Field) -> Optional[str]:
    return field.metadata.get("snippet_default")


@lru_cache(maxsize=None)
def dataclass_field_sensitive(field: Field) -> Tuple[Any, Any]:
    sensitive = field.metadata.get("sensitive", MISSING)

    if sensitive is True:
        field_type = field.type
        if field_type is Any:
            field_type = type(None)
        field_type_args = getattr(field_type, "__args__", ())
        field_type = getattr(field_type, "__origin__", field_type)
        if (
            field_type is Union
            and len(field_type_args) == 2
            and field_type_args[1] is type(None)
        ):
            field_type = field_type_args[0]
            field_type = getattr(field_type, "__origin__", field_type)
        if issubclass(field_type, (list, set)):
            return MISSING, (lambda: field_type((REDACTED_TEXT,)))
        elif issubclass(field_type, dict):
            return (
                MISSING,
                (lambda: field_type(((REDACTED_TEXT, REDACTED_TEXT),))),
            )
        else:
            return REDACTED_TEXT, MISSING

    sensitive_factory = field.metadata.get("sensitive_factory", MISSING)
    return sensitive, sensitive_factory


class ToDict(dict):
    """
    We use a dictionary to cache the object type > converter mapping, this
    prevents us from having to do potentially expensive isinstance checks for
    known objects.
    """

    def __getitem__(self, obj: Any) -> Callable:
        obj_type = type(obj)
        converter = super().get(obj_type)
        if converter is None:
            converter = self._get_converter(obj_type)
            self.__setitem__(obj_type, converter)
        return converter

    def _get_converter(self, obj_type: Type) -> Callable:
        if issubclass(obj_type, str):
            return self._convert_str
        elif issubclass(obj_type, dict):
            return self._convert_dict
        elif issubclass(obj_type, (list, set)):
            return self._convert_list
        elif issubclass(obj_type, Enum):
            return self._convert_enum
        elif issubclass(obj_type, timedelta):
            return self._convert_timedelta
        elif issubclass(obj_type, float):
            return self._convert_float
        elif issubclass(obj_type, BinaryFile):
            return self._convert_default
        elif is_data_class(obj_type):
            return self._convert_dataclass
        else:
            return self._convert_default

    def _convert_str(
        self,
        obj: Any,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> str:
        return str(obj)

    def _convert_dict(
        self,
        obj: dict,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> dict:
        items = {}
        for key in obj:
            value = self[obj[key]](
                obj[key],
                preserve_nones=preserve_nones,
                to_camel_case_fields=to_camel_case_fields,
            )
            if value is not MISSING:
                items[
                    _to_dict[key](
                        key,
                        preserve_nones=preserve_nones,
                        to_camel_case_fields=to_camel_case_fields,
                    )
                ] = value
        return items

    def _convert_list(
        self,
        obj: list,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> list:
        items = []
        for item in obj:
            new_item = self[item](
                item,
                preserve_nones=preserve_nones,
                to_camel_case_fields=to_camel_case_fields,
            )
            if new_item is not MISSING:
                items.append(new_item)
        return items

    def _convert_enum(
        self,
        obj: Enum,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> Enum:
        return obj.value

    def _convert_timedelta(
        self,
        obj: timedelta,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> str:
        return from_timedelta(obj)

    def _convert_float(
        self,
        obj: Real,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> Union[Real, str]:
        if isinf(obj) or isnan(obj):
            return str(obj)
        return obj

    def _convert_dataclass(
        self,
        obj: Any,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> dict:
        kwargs = {}
        for field in dataclass_init_fields(type(obj)):
            key = field.name
            attr = getattr(obj, key)
            value = self[attr](
                attr,
                preserve_nones=preserve_nones,
                to_camel_case_fields=to_camel_case_fields,
            )
            if value is None:
                default, default_factory = dataclass_field_default(field)
                if (
                    (default is MISSING or default is None)
                    and default_factory is MISSING
                ) and not preserve_nones:
                    continue
            elif value is MISSING:
                continue
            explict_key = field.metadata.get("key")
            if explict_key:
                key = explict_key
            elif to_camel_case_fields:
                key = to_camel_case(key)
            kwargs[key] = value

        return kwargs

    def _convert_default(
        self,
        obj: Any,
        *,
        preserve_nones: bool = False,
        to_camel_case_fields: bool = False,
    ) -> Any:
        return obj


_to_dict = ToDict()


def to_dict(
    obj: Any,
    *,
    preserve_nones: bool = False,
    to_camel_case_fields: bool = False,
) -> Any:
    return _to_dict[obj](
        obj,
        preserve_nones=preserve_nones,
        to_camel_case_fields=to_camel_case_fields,
    )


def from_dict(
    target_type: type,
    obj: Any,
    *,
    from_camel_case_fields: bool = False,
    fail: bool = True,
    strict: bool = False,
) -> Any:
    # TODO helpful, contextual error handling (with little/no performance impact)
    if target_type is Any:
        target_type = type(None)

    target_type_args = getattr(target_type, "__args__", ())
    target_type = getattr(target_type, "__origin__", target_type)

    if target_type is Union:
        for union_type in target_type_args:
            result = from_dict(
                union_type,
                obj,
                from_camel_case_fields=from_camel_case_fields,
                fail=False,
                strict=strict,
            )
            if result is not MISSING:
                return result

    elif isinstance(obj, dict):
        if is_data_class(target_type):
            kwargs = {}
            for field in dataclass_init_fields(target_type):
                key = field.name
                default, default_factory = dataclass_field_default(field)
                explict_key = field.metadata.get("key")
                if explict_key:
                    key = explict_key
                elif from_camel_case_fields:
                    key = to_camel_case(key)
                if key in obj:
                    value = obj[key]
                    skip_convert = False
                elif default is not MISSING:
                    value = default
                    skip_convert = True
                elif default_factory is not MISSING:
                    value = default_factory()
                    skip_convert = True
                else:
                    value = None
                    skip_convert = False
                if value is MISSING:
                    continue
                elif skip_convert:
                    new_value = value
                else:
                    new_type = field.type
                    sensitive, sensitive_factory = dataclass_field_sensitive(
                        field
                    )
                    if (
                        sensitive is not MISSING
                        or sensitive_factory is not MISSING
                    ) and isinstance(value, dict):
                        new_type = Union[SensitiveDataRef, new_type]
                    new_value = from_dict(
                        new_type,
                        value,
                        from_camel_case_fields=from_camel_case_fields,
                        fail=fail,
                        strict=strict,
                    )
                    if new_value is MISSING:
                        return MISSING
                kwargs[field.name] = new_value
            return target_type(**kwargs)

        elif issubclass(target_type, dict):
            (key_type, value_type) = target_type_args or (Any, Any)
            items = {}
            for key in obj:
                value = obj[key]
                new_key = from_dict(
                    key_type,
                    key,
                    from_camel_case_fields=from_camel_case_fields,
                    fail=fail,
                    strict=strict,
                )
                if new_key is MISSING:
                    return MISSING
                if value is MISSING:
                    continue
                else:
                    new_value = from_dict(
                        value_type,
                        value,
                        from_camel_case_fields=from_camel_case_fields,
                        fail=fail,
                        strict=strict,
                    )
                    if new_value is MISSING:
                        return MISSING
                items[new_key] = new_value
            if target_type is dict:
                return items
            else:
                return target_type(items)

        else:
            return obj

    elif strict and is_data_class(target_type) and not isinstance(obj, dict):
        fail = True

    elif isinstance(obj, list):
        if issubclass(target_type, list) or issubclass(target_type, set):
            (item_type,) = target_type_args or (Any,)
            items = []
            for item in obj:
                if item is not MISSING:
                    new_item = from_dict(
                        item_type,
                        item,
                        from_camel_case_fields=from_camel_case_fields,
                        fail=fail,
                        strict=strict,
                    )
                    if new_item is MISSING:
                        return MISSING
                    items.append(new_item)
            if target_type is list:
                return items
            else:
                return target_type(items)

        else:
            return obj

    elif isinstance(obj, str):
        if issubclass(target_type, Enum):
            try:
                return target_type(obj)
            except ValueError:
                pass

        elif issubclass(target_type, timedelta):
            try:
                return to_timedelta(obj)
            except ValueError:
                pass

        elif issubclass(float, target_type) and obj in ("inf", "-inf", "nan"):
            return float(obj)

        elif issubclass(target_type, str):
            return target_type(obj)

        else:
            return obj

    elif obj is None:
        if target_type is type(None):
            return None

    else:
        return obj

    if fail:
        raise ValueError(f"mismatch for {target_type} and {obj}")
    else:
        return MISSING
