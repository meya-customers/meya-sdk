import re

from colored import attr
from colored import fg
from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from datetime import timedelta
from enum import Enum
from functools import lru_cache
from meya.core.base_ref import BaseRef
from meya.core.phase import Phase
from meya.core.source_location import SourceLocation
from meya.core.template import Template
from meya.core.template_registry import TemplateRegistry
from meya.core.template_registry import TemplateRegistryRenderError
from meya.core.type_registry import TypeRegistry
from meya.element import AbstractSpecRegistry
from meya.element import Element
from meya.element import Ref
from meya.element import Spec
from meya.element.element import AnyRef
from meya.element.element_error import ElementImportError
from meya.element.element_error import ElementParseError
from meya.element.element_error import ElementTemplateError
from meya.element.element_error import ElementValidationError
from meya.flow.element import Flow
from meya.flow.element import FlowRef
from meya.flow.element import StepLabel
from meya.flow.element import StepLabelRef
from meya.time.timedelta import to_timedelta
from meya.trigger.element import Trigger
from meya.trigger.element import TriggerActionEntry
from meya.trigger.element.element import ComponentTriggerSpec
from meya.trigger.element.element import FlowTriggerSpec
from meya.util.dict import dataclass_field_default
from meya.util.dict import dataclass_init_fields
from meya.util.dict import from_dict
from meya.util.dict import is_data_class
from meya.util.dict import to_dict
from meya.util.template import CustomNativeTemplate
from meya.util.template import from_template_async
from meya.util.yaml import LineCol
from pathlib import Path
from ruamel.yaml.comments import CommentedMap
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

EXCLUDED_SPEC_KEYS = {"id", "type", "timeout"}


@dataclass
class SpecRegistry(AbstractSpecRegistry):
    items: Dict[str, Spec]
    top_level_refs: List[Ref] = field(default_factory=list)

    template_items: Dict[str, Spec] = field(init=False, default_factory=list)
    refs: List[Tuple[Ref, SourceLocation]] = field(
        init=False, default_factory=list
    )
    step_label_refs: List[
        Tuple[StepLabelRef, FlowRef, SourceLocation]
    ] = field(init=False, default_factory=list)

    def append(self, spec: Spec) -> None:
        self.items[spec.id] = spec
        self.top_level_refs.append(Ref(spec.id))

    def resolve(self, ref: Ref) -> Spec:
        return self.items[ref.ref]

    def try_resolve(self, ref: Ref) -> Optional[Spec]:
        return self.items.get(ref.ref, None)

    def find_top_level_refs(self, ref_type: Type[AnyRef]) -> List[AnyRef]:
        if ref_type is Ref:
            return [Ref(ref.ref) for ref in self.top_level_refs]

        ref_element_types = set(
            element_type.get_element_type()
            for element_type in TypeRegistry.current.get().items
            if issubclass(element_type, ref_type.element_type)
        )
        top_level_ids = set(ref.ref for ref in self.top_level_refs)
        return [
            ref_type(spec.id)
            for spec in self.items.values()
            if spec.id in top_level_ids and spec.type in ref_element_types
        ]

    def validate(self) -> None:
        for spec in self.items.values():
            if not spec.is_partial:
                Element.validate_from_spec(spec)
        for ref, source_location in self.refs:
            ref.validate(source_location)
        for step_label_ref, flow_ref, source_location in self.step_label_refs:
            step_label_ref.validate(flow_ref, source_location)

    async def render(self, context: dict, ref: Ref) -> Spec:
        render_items: Dict[str, Spec] = {}
        render_refs: List[Tuple[Ref, SourceLocation]] = []
        render_step_label_refs: List[
            Tuple[StepLabelRef, FlowRef, SourceLocation]
        ] = []
        spec = self.template_items[ref.ref]
        await self._extract_obj(
            context=context,
            items=self.items,
            template_items=render_items,
            refs=render_refs,
            step_label_refs=render_step_label_refs,
            source_location=spec.source_location,
            content=spec.data,
            target_type=Spec,
            phase=Phase.PROCESS_ENTRY,
            parent_data_type=None,
            parent_data_key=None,
            parent_flow_id=spec.parent_flow_id,
            spec_id=lambda: spec.id,
            template_found=lambda: None,
            fail=True,
        )
        assert len(render_items) > 0
        for render_ref, source_location in render_refs:
            render_ref.validate(source_location)
        for (
            render_step_label_ref,
            flow_ref,
            source_location,
        ) in render_step_label_refs:
            render_step_label_ref.validate(flow_ref, source_location)
        return render_items[ref.ref]

    @classmethod
    async def extract(cls):
        context = None
        items = {}
        template_items = {}
        refs = []
        step_label_refs = []
        top_level_refs = []
        for template in TemplateRegistry.current.get().items:
            await cls._extract_template(
                context,
                items,
                template_items,
                refs,
                step_label_refs,
                top_level_refs,
                template,
            )
        spec_registry = cls(items, top_level_refs=top_level_refs)
        spec_registry.template_items = template_items
        spec_registry.refs = refs
        spec_registry.step_label_refs = step_label_refs
        return spec_registry

    @classmethod
    async def _extract_template(
        cls,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        top_level_refs: List[Ref],
        template: Template,
    ):
        source_location = template.source_location
        spec_id = template.content.get("id")
        if spec_id is None:
            if template.single_document:
                spec_id = ".".join(
                    Path(source_location.file_path).with_suffix("").parts
                )
        if not isinstance(spec_id, str):
            raise ElementParseError(
                source_location, "'id' required for multi-document YAML files"
            )
        top_level_refs.append(Ref(spec_id))
        await cls._extract_obj(
            context=context,
            items=items,
            template_items=template_items,
            refs=refs,
            step_label_refs=step_label_refs,
            source_location=source_location,
            content=template.content,
            target_type=Spec,
            phase=Phase.LOAD_APP,
            parent_data_type=None,
            parent_data_key=None,
            parent_flow_id=None,
            spec_id=lambda: spec_id,
            template_found=lambda: None,
            fail=True,
        )

    @classmethod
    async def _extract_obj(
        cls,
        *,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        source_location: SourceLocation,
        content: Any,
        target_type: Type,
        phase: Phase,
        parent_data_type: Optional[Type],
        parent_data_key: Optional[str],
        parent_flow_id: Optional[str],
        spec_id: Callable[[], str],
        template_found: Callable[[], None],
        fail: bool,
    ):
        def raise_template_error(e: Exception):
            if parent_data_type and parent_data_key:
                raise ElementTemplateError(
                    source_location=source_location,
                    message=f"{str(e)} in {parent_data_type.__name__}.{parent_data_key} template",
                )
            else:
                raise ElementTemplateError(
                    source_location=source_location,
                    message=f"{str(e)} in template",
                )

        if isinstance(content, CustomNativeTemplate):
            if phase is Phase.LOAD_APP:
                template_found()
                return content

            try:
                content = await from_template_async(context, content)
            except Exception as e:
                raise_template_error(e)
        elif isinstance(content, TemplateRegistryRenderError):
            raise_template_error(content.error)

        extract_method = cls._find_extract_method(target_type, type(content))

        if extract_method:
            result = await extract_method(
                context=context,
                items=items,
                template_items=template_items,
                refs=refs,
                step_label_refs=step_label_refs,
                source_location=source_location,
                content=content,
                target_type=target_type,
                phase=phase,
                parent_data_type=parent_data_type,
                parent_data_key=parent_data_key,
                parent_flow_id=parent_flow_id,
                spec_id=spec_id,
                template_found=template_found,
                fail=fail,
            )
            if result is not MISSING:
                return result

        if fail:
            problem = "missing" if content is None else "not a valid"
            target_type_names = cls._join_union_type_names(target_type)
            if parent_data_type and parent_data_key:
                raise ElementValidationError(
                    source_location,
                    f"{problem} {target_type_names} for"
                    f" {parent_data_type.__name__}.{parent_data_key}",
                )
            else:
                raise ElementValidationError(
                    source_location, f"{problem} {target_type_names}"
                )
        else:
            return MISSING

    @classmethod
    @lru_cache(maxsize=None)
    def _find_extract_method(cls, target_type: Type, content_type: Type):
        target_type_origin = getattr(target_type, "__origin__", None)

        if target_type_origin is Union:
            extract_methods = []
            # noinspection PyUnresolvedReferences
            for union_type in target_type.__args__:
                extract_method = cls._find_extract_method(
                    union_type, content_type
                )
                if extract_method:
                    extract_methods.append(
                        cls._override_extract_method_type(
                            extract_method, union_type
                        )
                    )
            if len(extract_methods) == 1:
                return extract_methods[0]
            else:

                async def extract_union(
                    *,
                    context: Optional[dict],
                    items: Dict[str, Spec],
                    template_items: Dict[str, Spec],
                    refs: List[Tuple[Ref, SourceLocation]],
                    step_label_refs: List[
                        Tuple[StepLabelRef, FlowRef, SourceLocation]
                    ],
                    source_location: SourceLocation,
                    content: Any,
                    phase: Phase,
                    parent_data_type: Optional[Type],
                    parent_data_key: Optional[str],
                    parent_flow_id: Optional[str],
                    spec_id: Callable[[], str],
                    template_found: Callable[[], None],
                    **_kwargs,
                ):
                    for extract_union_method in extract_methods:
                        result = await extract_union_method(
                            context=context,
                            items=items,
                            template_items=template_items,
                            refs=refs,
                            step_label_refs=step_label_refs,
                            source_location=source_location,
                            content=content,
                            target_type=union_type,
                            phase=phase,
                            parent_data_type=parent_data_type,
                            parent_data_key=parent_data_key,
                            parent_flow_id=parent_flow_id,
                            spec_id=spec_id,
                            template_found=template_found,
                            fail=False,
                        )
                        if result is not MISSING:
                            return result
                    return MISSING

                return extract_union

        elif target_type is Any or (
            target_type_origin is None
            and issubclass(content_type, target_type)
        ):
            if issubclass(content_type, list):
                return cls._override_extract_method_type(
                    cls._extract_list, List[Any]
                )
            elif issubclass(content_type, dict):
                return cls._override_extract_method_type(
                    cls._extract_dict, Dict[Any, Any]
                )
            else:
                return cls._extract_basic

        elif target_type_origin is list:
            if issubclass(content_type, list):
                return cls._extract_list

        elif target_type_origin is dict:
            if issubclass(content_type, dict):
                return cls._extract_dict

        elif issubclass(target_type, StepLabel):
            if issubclass(content_type, str):
                return cls._extract_step_label

        elif issubclass(target_type, BaseRef):
            if issubclass(content_type, str):
                return cls._extract_base_ref

        elif issubclass(target_type, TriggerActionEntry):
            # Trigger action entries can't be specified in BFML
            return None

        elif issubclass(target_type, Enum):
            if issubclass(content_type, str):
                return cls._extract_enum

        elif issubclass(target_type, timedelta):
            if issubclass(content_type, str):
                return cls._extract_timedelta

        elif issubclass(target_type, str):
            if issubclass(content_type, str):
                return cls._extract_str

        elif issubclass(target_type, Spec):
            if issubclass(content_type, (dict, str)):
                return cls._extract_spec

        elif is_data_class(target_type):
            if issubclass(content_type, dict):
                return cls._extract_data_type

        return None

    @classmethod
    def _override_extract_method_type(
        cls, extract_method, target_type_override
    ):
        async def extract_override(
            *,
            context: Optional[dict],
            items: Dict[str, Spec],
            template_items: Dict[str, Spec],
            refs: List[Tuple[Ref, SourceLocation]],
            step_label_refs: List[
                Tuple[StepLabelRef, FlowRef, SourceLocation]
            ],
            source_location: SourceLocation,
            content: Any,
            phase: Phase,
            parent_data_type: Optional[Type],
            parent_data_key: Optional[str],
            parent_flow_id: Optional[str],
            spec_id: Callable[[], str],
            template_found: Callable[[], None],
            fail: bool,
            **_kwargs,
        ):
            return await extract_method(
                context=context,
                items=items,
                template_items=template_items,
                refs=refs,
                step_label_refs=step_label_refs,
                source_location=source_location,
                content=content,
                target_type=target_type_override,
                phase=phase,
                parent_data_type=parent_data_type,
                parent_data_key=parent_data_key,
                parent_flow_id=parent_flow_id,
                spec_id=spec_id,
                template_found=template_found,
                fail=fail,
            )

        return extract_override

    @classmethod
    def _join_union_type_names(cls, union_type: Type):
        # noinspection PyUnresolvedReferences
        union_items = (
            union_type.__args__
            if getattr(union_type, "__origin__", None) is Union
            else (union_type,)
        )
        return " or ".join(
            re.sub(r"\w+\.+", "", repr(union_item))
            if hasattr(union_item, "__origin__")
            else union_item.__name__
            for union_item in union_items
            if union_item not in [type(None), TriggerActionEntry]
        )

    @classmethod
    async def _extract_basic(cls, *, content: Any, **_kwargs):
        return content

    @classmethod
    async def _extract_list(
        cls,
        *,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        source_location: SourceLocation,
        content: Any,
        target_type: Type,
        phase: Phase,
        parent_data_type: Optional[Type],
        parent_data_key: Optional[str],
        parent_flow_id: Optional[str],
        spec_id: Callable[[], str],
        template_found: Callable[[], None],
        fail: bool,
    ):
        # noinspection PyUnresolvedReferences
        (item_type,) = target_type.__args__
        result = []
        for i in range(len(content)):
            content_item = content[i]
            item = await cls._extract_obj(
                context=context,
                items=items,
                template_items=template_items,
                refs=refs,
                step_label_refs=step_label_refs,
                source_location=source_location.for_yaml_item(content, i),
                content=content_item,
                target_type=item_type,
                phase=phase,
                parent_data_type=parent_data_type,
                parent_data_key=parent_data_key,
                parent_flow_id=parent_flow_id,
                spec_id=lambda: f"{spec_id()}.{i}",
                template_found=template_found,
                fail=fail,
            )
            if item is MISSING:
                return MISSING
            result.append(item)
        return result

    @classmethod
    async def _extract_dict(
        cls,
        *,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        source_location: SourceLocation,
        content: Any,
        target_type: Type,
        phase: Phase,
        parent_data_type: Optional[Type],
        parent_data_key: Optional[str],
        parent_flow_id: Optional[str],
        spec_id: Callable[[], str],
        template_found: Callable[[], None],
        fail: bool,
    ):
        # noinspection PyUnresolvedReferences
        (key_type, value_type) = target_type.__args__
        result = {}
        for i, content_key in enumerate(content.keys()):
            content_value = content[content_key]
            if not isinstance(content_key, CustomNativeTemplate):
                spec_id_key = lambda: f".{content_key}"
            else:
                spec_id_key = lambda: f":index.{i}"
            key = await cls._extract_obj(
                context=context,
                items=items,
                template_items=template_items,
                refs=refs,
                step_label_refs=step_label_refs,
                source_location=source_location.for_yaml_key(
                    content, content_key
                ),
                content=content_key,
                target_type=key_type,
                phase=phase,
                parent_data_type=parent_data_type,
                parent_data_key=parent_data_key,
                parent_flow_id=parent_flow_id,
                spec_id=lambda: f"{spec_id()}:key{spec_id_key()}",
                template_found=template_found,
                fail=fail,
            )
            if key is MISSING:
                return MISSING
            value = await cls._extract_obj(
                context=context,
                items=items,
                template_items=template_items,
                refs=refs,
                step_label_refs=step_label_refs,
                source_location=source_location.for_yaml_value(
                    content, content_key
                ),
                content=content_value,
                target_type=value_type,
                phase=phase,
                parent_data_type=parent_data_type,
                parent_data_key=parent_data_key,
                parent_flow_id=parent_flow_id,
                spec_id=lambda: f"{spec_id()}{spec_id_key()}",
                template_found=template_found,
                fail=True,
            )
            if value is MISSING:
                return MISSING
            result[key] = value
        return result

    @classmethod
    async def _extract_step_label(cls, *, content: Any, **_kwargs):
        if content.startswith("(") and content.endswith(")"):
            return to_dict(StepLabel(content[1:-1]))
        else:
            return MISSING

    @classmethod
    async def _extract_base_ref(
        cls,
        *,
        source_location: SourceLocation,
        refs: List[Tuple[Ref, SourceLocation]],
        content: Any,
        target_type: Type,
        **_kwargs,
    ):
        ref = target_type(content)
        if isinstance(ref, Ref):
            refs.append((ref, source_location))
        return to_dict(ref)

    @classmethod
    async def _extract_enum(
        cls, *, content: Any, target_type: Type, **_kwargs
    ):
        try:
            return to_dict(target_type(content))
        except ValueError:
            return MISSING

    @classmethod
    async def _extract_timedelta(
        cls, *, content: Any, target_type: Type, **_kwargs
    ):
        try:
            return to_dict(to_timedelta(content))
        except ValueError:
            return MISSING

    @classmethod
    async def _extract_str(cls, *, content: Any, target_type: Type, **_kwargs):
        return target_type(content)

    @classmethod
    async def _extract_spec(
        cls,
        *,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        source_location: SourceLocation,
        content: Any,
        target_type: Type,
        phase: Phase,
        parent_flow_id: Optional[str],
        spec_id: Callable[[], str],
        fail: bool,
        **_kwargs,
    ):
        current_spec_id = spec_id()
        if phase is Phase.PROCESS_ENTRY:
            spec = items.get(current_spec_id, None)
            if spec and not spec.is_partial:
                return {"id": current_spec_id}

        # noinspection PyUnresolvedReferences
        target_element_type = target_type.element_type
        if isinstance(content, dict):
            element_alias = content.get("type")
            if element_alias:
                element_type = TypeRegistry.current.get().alias.get(
                    element_alias
                )
                if not element_type:
                    raise ElementImportError(
                        source_location.for_yaml_value(content, "type"),
                        f'no such element type "{element_alias}"',
                    )
            else:
                data_content = {}
                for key in content:
                    value = content[key]
                    if key not in EXCLUDED_SPEC_KEYS:
                        data_content[key] = value
                element_type = TypeRegistry.current.get().match_signature(
                    data_content
                )
                if not element_type:
                    return MISSING

        elif isinstance(content, str):
            element_alias = content
            element_type = TypeRegistry.current.get().alias.get(element_alias)
            if not element_type or not issubclass(element_type, Element):
                raise ElementImportError(
                    source_location, f'no such element "{element_alias}"'
                )
            content = {}

        else:
            return MISSING

        element_alias = element_type.get_element_type()

        if not issubclass(element_type, target_element_type):
            return MISSING
        if issubclass(target_element_type, Trigger) and parent_flow_id:
            if issubclass(target_type, ComponentTriggerSpec):
                if "action" not in content:
                    new_content_action = "next"
                    new_content = CommentedMap(
                        content, action=new_content_action
                    )
                    setattr(
                        new_content,
                        LineCol.attrib,
                        cls._copy_lc(content, "action"),
                    )
                    content = new_content
            elif issubclass(target_type, FlowTriggerSpec):
                if "action" not in content:
                    new_content_action = CommentedMap(flow=parent_flow_id)
                    new_content_action.lc.line = source_location.line
                    new_content_action.lc.col = source_location.column
                    new_content_action.lc.add_kv_line_col(
                        "flow",
                        [
                            source_location.line,
                            source_location.column,
                            source_location.line,
                            source_location.column,
                        ],
                    )
                    new_content = CommentedMap(
                        content, action=new_content_action
                    )
                    setattr(
                        new_content,
                        LineCol.attrib,
                        cls._copy_lc(content, "action"),
                    )
                    content = new_content
                elif (
                    isinstance(content["action"], dict)
                    and "type" not in content["action"]
                    and "flow" not in content["action"]
                ):
                    new_content_action = CommentedMap(
                        content["action"], flow=parent_flow_id
                    )
                    setattr(
                        new_content_action,
                        LineCol.attrib,
                        cls._copy_lc(content["action"], "flow"),
                    )
                    new_content = CommentedMap(
                        content, action=new_content_action
                    )
                    setattr(
                        new_content,
                        LineCol.attrib,
                        getattr(content, LineCol.attrib, None) or LineCol(),
                    )
                    content = new_content
        timeout = content.get("timeout", None)
        if timeout is not None and not isinstance(timeout, int):
            raise ElementValidationError(
                source_location.for_yaml_value(content, "timeout"),
                f"not a valid int for Spec.timeout",
            )
        elif timeout:
            print(
                f"{fg('light_salmon_3b') + attr('bold')}"
                f"w {current_spec_id} custom timeout is no longer supported"
            )

        if issubclass(element_type, Flow):
            next_parent_flow_id = current_spec_id
        else:
            next_parent_flow_id = parent_flow_id

        template_found = False

        def set_template_found():
            nonlocal template_found
            template_found = True

        data_content = CommentedMap()
        for key in content:
            value = content[key]
            if key not in EXCLUDED_SPEC_KEYS:
                data_content[key] = value
        setattr(
            data_content,
            LineCol.attrib,
            getattr(content, LineCol.attrib, None),
        )

        result = await cls._extract_data_type(
            context=context,
            items=items,
            template_items=template_items,
            refs=refs,
            step_label_refs=step_label_refs,
            source_location=source_location,
            content=data_content,
            target_type=element_type,
            phase=phase,
            parent_flow_id=next_parent_flow_id,
            spec_id=lambda: current_spec_id,
            template_found=set_template_found,
            fail=fail,
        )

        if result is MISSING:
            return MISSING

        if phase is Phase.LOAD_APP:
            if not template_found:
                items[current_spec_id] = Spec(
                    type=element_alias,
                    data=result,
                    id=current_spec_id,
                    source_location=source_location,
                    timeout=timeout,
                )
            else:
                items[current_spec_id] = Spec(
                    type=element_alias,
                    data=None,
                    id=current_spec_id,
                    source_location=source_location,
                    timeout=timeout,
                )
                template_items[current_spec_id] = Spec(
                    type=element_alias,
                    data=content,
                    id=current_spec_id,
                    source_location=source_location,
                    timeout=timeout,
                    parent_flow_id=parent_flow_id,
                )
            return {"id": current_spec_id}
        else:
            spec = Spec(
                type=element_alias,
                data=result,
                id=current_spec_id,
                source_location=source_location,
                timeout=timeout,
            )
            template_items[current_spec_id] = spec
            return to_dict(spec)

    @classmethod
    def _copy_lc(cls, obj: dict, new_key: str):
        obj_lc = getattr(obj, LineCol.attrib, None)
        if obj_lc is not None:
            new_lc = LineCol()
            new_lc.line = obj_lc.line
            new_lc.col = obj_lc.col
            new_lc.data = dict(obj_lc.data)
            new_lc.add_kv_line_col(
                new_key, [obj_lc.line, obj_lc.col, obj_lc.line, obj_lc.col]
            )
        else:
            return None

    @classmethod
    async def _extract_data_type(
        cls,
        *,
        context: Optional[dict],
        items: Dict[str, Spec],
        template_items: Dict[str, Spec],
        refs: List[Tuple[Ref, SourceLocation]],
        step_label_refs: List[Tuple[StepLabelRef, FlowRef, SourceLocation]],
        source_location: SourceLocation,
        content: Any,
        target_type: Type,
        phase: Phase,
        parent_flow_id: Optional[str],
        spec_id: Callable[[], str],
        template_found: Callable[[], None],
        fail: bool,
        **_kwargs,
    ):
        content_flow_ref = None
        content_step_label_refs = []
        extra_keys = set()
        for content_key in content:
            extra_keys.add(content_key)
        data = {}
        for init_field in dataclass_init_fields(target_type):
            key = init_field.name
            default, default_factory = dataclass_field_default(init_field)
            if (
                init_field.metadata.get("from_context")
                and init_field.type is FlowRef
            ):
                content_flow_ref = FlowRef(parent_flow_id)
                data[key] = to_dict(content_flow_ref)
            else:
                explict_key = init_field.metadata.get("key")
                if explict_key:
                    content_key = explict_key
                    data_key = content_key
                else:
                    content_key = TypeRegistry.remove_trailing_underscore(key)
                    data_key = key
                    # TODO Support nested dataclasses in elements with trailing underscore fields
                if content_key in content:
                    content_source_location = source_location.for_yaml_value(
                        content, content_key
                    )
                    value = await cls._extract_obj(
                        context=context,
                        items=items,
                        template_items=template_items,
                        refs=refs,
                        step_label_refs=step_label_refs,
                        source_location=content_source_location,
                        content=content[content_key],
                        target_type=init_field.type,
                        phase=phase,
                        parent_data_type=target_type,
                        parent_data_key=content_key,
                        parent_flow_id=parent_flow_id,
                        spec_id=lambda: f"{spec_id()}.{content_key}",
                        template_found=template_found,
                        fail=fail,
                    )
                    if value is MISSING:
                        return MISSING
                    data[data_key] = value
                    extra_keys.remove(content_key)
                    if (
                        init_field.type is FlowRef
                        and data[data_key] is not None
                    ):
                        content_flow_ref = from_dict(FlowRef, data[data_key])
                    elif (
                        init_field.type is StepLabelRef
                        or (
                            getattr(init_field.type, "__origin__", None)
                            is Union
                            and StepLabelRef in init_field.type.__args__
                        )
                    ) and data[data_key] is not None:
                        content_step_label_refs.append(
                            (
                                from_dict(StepLabelRef, data[key]),
                                content_source_location,
                            )
                        )

                elif default is MISSING and default_factory is MISSING:
                    if fail:
                        raise ElementValidationError(
                            source_location,
                            f'missing key "{content_key}" for {target_type.__name__}',
                        )
                    else:
                        return MISSING

        if extra_keys:
            if fail:
                extra_key = list(extra_keys)[0]
                raise ElementValidationError(
                    source_location.for_yaml_key(content, extra_key),
                    f'unexpected key "{extra_key}" for {target_type.__name__}',
                )
            else:
                return MISSING

        if content_flow_ref is not None and not isinstance(
            content_flow_ref, CustomNativeTemplate
        ):
            for (
                content_step_label_ref,
                content_source_location,
            ) in content_step_label_refs:
                if not isinstance(
                    content_step_label_ref, CustomNativeTemplate
                ):
                    step_label_refs.append(
                        (
                            content_step_label_ref,
                            content_flow_ref,
                            content_source_location,
                        )
                    )

        return data
