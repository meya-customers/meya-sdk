from dataclasses import dataclass
from jinja2 import TemplateSyntaxError
from jinja2.ext import babel_extract
from meya.core.source import Source
from meya.core.source_location import SourceLocation
from meya.core.source_registry import SourceRegistry
from meya.core.template import Template
from meya.db.view.user import UserView
from meya.element.element_error import ElementParseError
from meya.util.context_var import ScopedContextVar
from meya.util.template import environment
from meya.util.template import from_template_async
from meya.util.template import jinja2_options
from meya.util.template import to_template_async
from meya.util.undefined import MISSING_UNDEFINED
from meya.util.undefined import MissingUndefinedError
from meya.util.yaml import LineCol
from meya.util.yaml import from_multi_yaml
from ruamel.yaml.comments import CommentedBase
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.comments import CommentedSeq
from ruamel.yaml.error import MarkedYAMLError
from typing import Any
from typing import ClassVar
from typing import List
from typing import cast


@dataclass
class TemplateRegistry:
    items: List[Template]

    current: ClassVar = cast(
        ScopedContextVar["TemplateRegistry"], ScopedContextVar()
    )

    @classmethod
    async def parse_and_try_render(cls, context: dict) -> "TemplateRegistry":
        with UserView.current.set(MISSING_UNDEFINED):
            items = []
            for source in SourceRegistry.current.get().items:
                definitions = cls._parse_yaml(source)
                for definition in definitions:
                    items.append(
                        await cls._parse_and_try_render_definition_templates(
                            context,
                            source.file_path,
                            definition,
                            len(definitions) == 1,
                        )
                    )
            return cls(items)

    @classmethod
    def _parse_yaml(cls, source: Source) -> List[Any]:
        try:
            return list(from_multi_yaml(source.text))
        except MarkedYAMLError as error:
            source_location = SourceLocation(
                source.file_path,
                error.problem_mark.line,
                error.problem_mark.column,
            )
            raise ElementParseError(source_location, error.problem)

    @classmethod
    async def _parse_and_try_render_definition_templates(
        cls,
        context: dict,
        file_path: str,
        definition: Any,
        single_document: bool,
    ) -> Template:
        if isinstance(definition, CommentedBase):
            source_location = SourceLocation(
                file_path, definition.lc.line, definition.lc.col
            )
        else:
            # Non-collections don't have any source location from ruamel.yaml
            source_location = SourceLocation(file_path, line=0, column=None)
        if not isinstance(definition, CommentedMap):
            raise ElementParseError(source_location, f"not a YAML mapping")
        return Template(
            await cls._parse_and_try_render_obj_templates(
                context, source_location, definition
            ),
            single_document,
            source_location,
        )

    @classmethod
    async def _parse_and_try_render_obj_templates(
        cls, context: dict, source_location: SourceLocation, content: Any
    ):
        if isinstance(content, str):
            try:
                template = to_template_async(content)
            except TemplateSyntaxError as error:
                source_location = SourceLocation(
                    source_location.file_path,
                    source_location.line + error.lineno - 1,
                    column=None,
                )
                raise ElementParseError(source_location, error.message)
            try:
                return await from_template_async(context, template)
            except MissingUndefinedError:
                # If a key is missing during load, let the template get
                # reevaluated during process
                return template
            except Exception as e:
                # If there was any other error, let the spec registry format
                # it consistently
                return TemplateRegistryRenderError(e)

        elif isinstance(content, CommentedSeq):
            result = CommentedSeq()
            for i in range(len(content)):
                result.append(
                    await cls._parse_and_try_render_obj_templates(
                        context,
                        source_location.for_yaml_item(content, i),
                        content[i],
                    )
                )
            setattr(
                result, LineCol.attrib, getattr(content, LineCol.attrib, None)
            )
            return result

        elif isinstance(content, CommentedMap):
            content_lc = getattr(content, LineCol.attrib, None)
            result = CommentedMap()
            result_lc = LineCol()
            result_lc.line = content_lc.line
            result_lc.col = content_lc.col
            for content_key in content:
                result_key = await cls._parse_and_try_render_obj_templates(
                    context,
                    source_location.for_yaml_key(content, content_key),
                    content_key,
                )
                result_value = await cls._parse_and_try_render_obj_templates(
                    context,
                    source_location.for_yaml_value(content, content_key),
                    content[content_key],
                )
                result[result_key] = result_value
                result_lc.add_kv_line_col(
                    result_key, content_lc.data[content_key]
                )
            setattr(result, LineCol.attrib, result_lc)
            return result

        else:
            return content


@dataclass(frozen=True)
class TemplateRegistryRenderError:
    error: Exception


def extract_translations(fileobj, keywords, comment_tags, options):
    messages = []
    documents = from_multi_yaml(fileobj)
    for document in documents:
        _extract_translations_custom_from_content(messages, document)
    return messages


def _extract_translations_custom_from_content(
    messages: list, content: Any, line: int = 0
):
    if isinstance(content, str):
        template_messages = environment.extract_translations(content)
        for lineno, funcname, message in template_messages:
            comments = []
            if isinstance(message, tuple):
                message = tuple(part and part.strip() for part in message)
            elif message:
                message = message.strip()
            messages.append((line + lineno, funcname, message, comments))

    elif isinstance(content, CommentedSeq):
        for i, item in enumerate(content):
            [line, _] = (getattr(content, LineCol.attrib)).data[i]
            _extract_translations_custom_from_content(messages, item, line)

    elif isinstance(content, CommentedMap):
        for key, value in content.items():
            [key_line, _, value_line, _] = (
                getattr(content, LineCol.attrib)
            ).data[key]
            _extract_translations_custom_from_content(messages, key, key_line)
            _extract_translations_custom_from_content(
                messages, value, value_line
            )


def extract_jinja2_translations(
    fileobj, keywords, comment_tags, options: dict
):
    extensions = ",".join(
        [
            *(options.get("extensions", "").split(",")),
            *(jinja2_options.get("extensions", [])),
        ]
    )
    options.update(jinja2_options)
    options.update(extensions=extensions)
    options.update(undefined="StrictUndefined")
    options = {key: str(value) for key, value in options.items()}
    return babel_extract(fileobj, keywords, comment_tags, options)
