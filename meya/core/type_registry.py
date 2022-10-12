import inspect
import site
import sys

from dataclasses import dataclass
from dataclasses import fields
from enum import Enum
from importlib import import_module
from itertools import chain
from meya.app_config import AppConfig
from meya.core.abstract_type_registry import AbstractTypeRegistry
from meya.core.type_registry_error import TypeRegistryImportError
from meya.element import Element
from meya.entry import Entry
from meya.util.dict import dataclass_init_fields
from meya.util.pathspec import make_pathspec
from meya.util.pathspec import read_gitignore_lines
from meya.util.pathspec import subtract_pathspec
from meya.util.pathspec import walk_pathspec
from meya.util.template import CustomNativeTemplate
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union


@dataclass
class ElementSignature:
    signature_fields: Dict[str, Optional[Type[Enum]]]
    init_keys: Set[str]
    element_type: Type[Element]


@dataclass
class TypeRegistry(AbstractTypeRegistry):
    items: List[type]
    alias: Dict[str, type]
    reverse_alias: Dict[type, str]
    private: Dict[type, type]
    signature: List[ElementSignature]

    def match_signature(
        self, content: Dict[str, Any]
    ) -> Optional[Type[Element]]:
        ambiguous_match = False
        best_match = None
        best_match_element_type = None
        best_match_errors = None
        for signature in self.signature:
            signature_match = True
            for signature_key in signature.signature_fields:
                if signature_key not in content:
                    signature_match = False
                    break
                signature_type = signature.signature_fields[signature_key]
                content_value = content[signature_key]
                if signature_type and not isinstance(
                    content_value, CustomNativeTemplate
                ):
                    try:
                        signature_type(content_value)
                    except ValueError:
                        signature_match = False
                        break
            if signature_match:
                match = len(signature.signature_fields)
                errors = len(set(content.keys()) - signature.init_keys)
                if (
                    best_match is None
                    or errors < best_match_errors
                    or (errors == best_match_errors and match > best_match)
                    or (
                        errors == best_match_errors
                        and match == best_match
                        and issubclass(
                            best_match_element_type, signature.element_type
                        )
                    )
                ):
                    ambiguous_match = False
                    best_match = match
                    best_match_element_type = signature.element_type
                    best_match_errors = errors
                elif (
                    errors == best_match_errors
                    and match == best_match
                    and not issubclass(
                        best_match_element_type, signature.element_type
                    )
                    and not issubclass(
                        signature.element_type, best_match_element_type
                    )
                ):
                    ambiguous_match = True
        if ambiguous_match:
            return None
        else:
            return best_match_element_type

    @classmethod
    def import_and_index_for_app(
        cls, *root_packages: Any, app_config: Optional[AppConfig] = None
    ) -> "TypeRegistry":
        return cls._import_and_index(
            chain(
                cls._walk_app_packages(app_config),
                cls._walk_root_packages(*root_packages),
            )
        )

    @classmethod
    def import_and_index(cls, *root_packages: Any) -> "TypeRegistry":
        return cls._import_and_index(cls._walk_root_packages(*root_packages))

    @staticmethod
    def remove_trailing_underscore(name: str):
        if name.endswith("_"):
            return name[:-1]
        else:
            return name

    @classmethod
    def _walk_app_packages(
        cls, app_config: Optional[AppConfig]
    ) -> Iterator[str]:
        app_config = app_config or AppConfig.current.get()
        return cls._walk_package(
            app_config.package_path,
            package=app_config.package,
            with_gitignore=True,
        )

    @classmethod
    def _walk_root_packages(cls, *root_packages: Any) -> Iterator[str]:
        return chain.from_iterable(
            cls._walk_package(
                Path(root_package_path_or_module),
                package=root_package,
                with_gitignore=False,
            )
            if isinstance(root_package_path_or_module, str)
            else [root_package_path_or_module.__name__]
            for root_package in root_packages
            for root_package_path_or_module in getattr(
                root_package, "__path__", None
            )
            or [root_package]
        )

    @classmethod
    def _walk_package(
        cls, package_path: Path, *, package: Any, with_gitignore: bool
    ) -> Iterator[str]:
        pathspec = make_pathspec(["*.py", "!*_test.py"])
        if with_gitignore:
            pathspec = subtract_pathspec(
                pathspec=pathspec,
                ignore_pathspec=make_pathspec(read_gitignore_lines()),
            )
        file_paths = walk_pathspec(package_path, pathspec)
        module_names = (
            cls._get_module_name(package_path, package, file_path)
            for file_path in file_paths
        )
        return (module_name for module_name in module_names if module_name)

    @classmethod
    def _get_module_name(
        cls, package_path: Path, package: Any, file_path: Path
    ) -> str:
        relative_path = file_path.relative_to(package_path)
        relative_parts = list(relative_path.parts)
        relative_parts[-1] = inspect.getmodulename(relative_parts[-1])
        if relative_parts[-1] == "__init__":
            relative_parts = relative_parts[:-1]
        if isinstance(package, str):
            relative_parts = [package] + relative_parts
        elif package is not None:
            relative_parts = [package.__name__] + relative_parts
        return ".".join(relative_parts)

    @classmethod
    def _import_and_index(cls, module_names: Iterator[str]) -> "TypeRegistry":
        items, alias = cls._initial_import_and_index(module_names)
        reverse_alias = cls._reverse_index(alias)
        cls._index_extra(items, alias)
        signature = cls._index_signature(items)
        private = cls._index_private(items, alias, reverse_alias)
        subclasses = cls._index_subclasses(items)
        return cls(
            items=items,
            alias=alias,
            reverse_alias=reverse_alias,
            private=private,
            signature=signature,
            subclasses=subclasses,
        )

    @classmethod
    def _initial_import_and_index(
        cls, module_names: Iterator[str]
    ) -> Tuple[List[type], Dict[str, type]]:
        items: Set[type] = set()
        alias: Dict[str, type] = {}

        for module_name in module_names:
            module = cls._import_module(module_name)
            cls._index_module_items(items, alias, module)

        return list(items), alias

    @classmethod
    def _import_module(cls, module_name: str) -> Any:
        try:
            return import_module(module_name)
        except Exception as e:
            raise TypeRegistryImportError(
                f'Error importing "{module_name}"'
            ) from e

    @classmethod
    def _index_module_items(
        cls, items: Set[type], alias: Dict[str, type], module: Any
    ) -> None:
        class_members = cls._get_module_class_members(module)
        item_types = cls._filter_class_members(class_members)
        items.update(set(item_types))

        if len(item_types) == 1:
            item = item_types[0]
            item_alias = cls._get_module_alias(module)
            if item_alias:
                alias[item_alias] = item

    @classmethod
    def _get_module_class_members(cls, module: Any) -> List[type]:
        if hasattr(module, "__all__"):
            all_members = (
                getattr(module, member) for member in module.__all__
            )
            return [
                member for member in all_members if inspect.isclass(member)
            ]
        else:
            return [
                member
                for _, member in inspect.getmembers(module)
                if inspect.isclass(member)
                and member.__module__ == module.__name__
            ]

    @classmethod
    def _filter_class_members(cls, class_members: List[type]) -> List[type]:
        return [
            class_member
            for class_member in class_members
            if issubclass(class_member, (Element, Entry))
            and not inspect.isabstract(class_member)
        ]

    @classmethod
    def _get_module_alias(cls, module: Any) -> Optional[str]:
        alias = module.__name__
        if alias.startswith("meya_private."):
            return None
        alias = cls.remove_trailing_underscore(alias)
        alias = alias.replace(".element.", ".")
        return alias

    @classmethod
    def _reverse_index(cls, alias: Dict[str, type]) -> Dict[type, str]:
        reverse: Dict[type, str] = {}
        for item_alias, item in alias.items():
            old_reverse_alias = reverse.get(item)
            if not old_reverse_alias or len(item_alias) < len(
                old_reverse_alias
            ):
                reverse[item] = item_alias
        return reverse

    @classmethod
    def _index_extra(cls, items: List[type], alias: Dict[str, type]):
        for item in items:
            extra_alias = issubclass(item, Element) and item.get_extra_alias()
            if extra_alias:
                alias[extra_alias] = item

    @classmethod
    def _index_signature(cls, items: List[type]) -> List[ElementSignature]:
        signature: List[ElementSignature] = []
        for item in items:
            item_signature = issubclass(
                item, Element
            ) and cls._get_element_signature(item)
            if item_signature:
                signature.append(item_signature)
        return signature

    @classmethod
    def _get_element_signature(
        cls, element_type: Type[Element]
    ) -> Optional[ElementSignature]:
        init_fields = dataclass_init_fields(element_type)
        signature_fields = {
            cls.remove_trailing_underscore(
                field.name
            ): cls._get_element_signature_field_type(field.type)
            for field in init_fields
            if field.metadata["signature"]
        }
        if signature_fields:
            init_keys = {
                cls.remove_trailing_underscore(field.name)
                for field in init_fields
            }
            return ElementSignature(signature_fields, init_keys, element_type)
        else:
            return None

    @classmethod
    def _get_element_signature_field_type(
        cls, field_type: type
    ) -> Optional[Type[Enum]]:
        if getattr(field_type, "__origin__", None) is Union:
            field_types = field_type.__args__
        elif inspect.isclass(field_type):
            field_types = (field_type,)
        else:
            field_types = ()
        field_types = [
            field_type
            for field_type in field_types
            if inspect.isclass(field_type) and issubclass(field_type, Enum)
        ]
        assert len(field_types) <= 1, "Only one enum type signature allowed"
        return field_types[0] if field_types else None

    @classmethod
    def _index_private(
        cls,
        items: List[type],
        alias: Dict[str, type],
        reverse_alias: Dict[type, str],
    ) -> Dict[type, type]:
        private: Dict[type, type] = {}

        public_element_types = set(
            item for item in alias.values() if issubclass(item, Element)
        )
        private_element_types = {
            private_element_type.__name__: private_element_type
            for private_element_type in set(
                item for item in items if issubclass(item, Element)
            )
            - public_element_types
        }

        for public_element_type in public_element_types:
            private_element_type = private_element_types.get(
                public_element_type.__name__
            )
            if not private_element_type:
                continue

            cls._validate_private_element_type(
                private_element_type, public_element_type
            )
            private[public_element_type] = private_element_type
            reverse_alias[private_element_type] = reverse_alias[
                public_element_type
            ]

        return private

    @classmethod
    def _validate_private_element_type(
        cls,
        private_element_type: Type[Element],
        public_element_type: Type[Element],
    ) -> None:
        # Make sure private elements don't override (or specify) any init fields
        if (
            private_element_type.__annotations__
            is not public_element_type.__annotations__
        ):
            private_annotation_keys = set(
                private_element_type.__annotations__.keys()
            )
            init_keys = set(
                field.name
                for field in fields(private_element_type)
                if field.init
            )
            assert not (
                private_annotation_keys & init_keys
            ), f"{private_element_type} private init fields {private_annotation_keys & init_keys}"

    @classmethod
    def _index_subclasses(cls, items: List[type]) -> Dict[type, Set[type]]:
        subclasses: Dict[type, Set[type]] = {}
        for item in items:
            subclasses[item] = {item}
        for item in items:
            for parent in item.__mro__:
                if parent in subclasses:
                    subclasses[parent].add(item)
        return subclasses

    @staticmethod
    def add_sys_path(add_path: Path):
        site.addsitedir(add_path)

    @classmethod
    def unload_modules_for_path(cls, unload_path: Path):
        unload_parts = unload_path.parts

        all_sys_parts = [Path(sys_path).parts for sys_path in sys.path]

        for module_key, module in list(sys.modules.items()):
            module_file = getattr(module, "__file__", None)
            if module_file:
                module_parts = Path(module_file).parts
                unload_depth = 0
                unload = False
                for sys_parts in all_sys_parts:
                    if (
                        len(sys_parts) > unload_depth
                        and sys_parts == module_parts[: len(sys_parts)]
                    ):
                        unload_depth = len(sys_parts)
                        unload = sys_parts == unload_parts[: len(sys_parts)]
                if unload:
                    del sys.modules[module_key]
