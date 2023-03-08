import sys
import types
import warnings

from itertools import chain
from itertools import islice
from jinja2 import Environment
from jinja2 import Template
from jinja2 import TemplateSyntaxError
from jinja2 import UndefinedError
from jinja2 import nodes
from jinja2.compiler import CodeGenerator
from jinja2.compiler import has_safe_repr
from jinja2.utils import concat
from jinja2.utils import escape
from meya.util.translation import gettext
from meya.util.translation import ngettext
from meya.util.undefined import MissingUndefinedError
from meya.util.undefined import StrictUndefined
from typing import Any
from typing import Dict


def no_eval_native_concat(nodes):
    """Return a native Python type from the list of compiled nodes. If the
    result is a single node, its value is returned. Otherwise, the nodes are
    concatenated as strings without any attempt to parse Python literals.
    """
    head = list(islice(nodes, 2))

    if not head:
        return ""

    if len(head) == 1:
        return head[0]
    else:
        if isinstance(nodes, types.GeneratorType):
            nodes = chain(head, nodes)
        buffer = ""
        for node in nodes:
            buffer += str(node)
        return buffer


async def no_eval_native_concat_async(async_gen):
    rv = []

    async def collect():
        async for event in async_gen:
            rv.append(event)

    await collect()
    return no_eval_native_concat(rv)


class CustomNativeCodeGenerator(CodeGenerator):
    """A code generator which avoids injecting ``to_string()`` calls around the
    internal code Jinja uses to render templates.
    """

    def visit_Output(self, node, frame):
        """Same as :meth:`CodeGenerator.visit_Output`, but do not call
        ``to_string`` on output nodes in generated code.
        """
        if self.has_known_extends and frame.require_output_check:
            return

        finalize = self.environment.finalize
        finalize_context = getattr(finalize, "contextfunction", False)
        finalize_eval = getattr(finalize, "evalcontextfunction", False)
        finalize_env = getattr(finalize, "environmentfunction", False)

        if finalize is not None:
            if finalize_context or finalize_eval:
                const_finalize = None
            elif finalize_env:

                def const_finalize(x):
                    return finalize(self.environment, x)

            else:
                const_finalize = finalize
        else:

            def const_finalize(x):
                return x

        # If we are inside a frame that requires output checking, we do so.
        outdent_later = False

        if frame.require_output_check:
            self.writeline("if parent_template is None:")
            self.indent()
            outdent_later = True

        # Try to evaluate as many chunks as possible into a static string at
        # compile time.
        body = []

        for child in node.nodes:
            try:
                if const_finalize is None:
                    raise nodes.Impossible()

                const = child.as_const(frame.eval_ctx)
                if not has_safe_repr(const):
                    raise nodes.Impossible()
            except nodes.Impossible:
                body.append(child)
                continue

            # the frame can't be volatile here, because otherwise the as_const
            # function would raise an Impossible exception at that point
            try:
                if frame.eval_ctx.autoescape:
                    if hasattr(const, "__html__"):
                        const = const.__html__()
                    else:
                        const = escape(const)

                const = const_finalize(const)
            except Exception:
                # if something goes wrong here we evaluate the node at runtime
                # for easier debugging
                body.append(child)
                continue

            if body and isinstance(body[-1], list):
                body[-1].append(const)
            else:
                body.append([const])

        # if we have less than 3 nodes or a buffer we yield or extend/append
        if len(body) < 3 or frame.buffer is not None:
            if frame.buffer is not None:
                # for one item we append, for more we extend
                if len(body) == 1:
                    self.writeline("%s.append(" % frame.buffer)
                else:
                    self.writeline("%s.extend((" % frame.buffer)

                self.indent()

            for item in body:
                if isinstance(item, list):
                    val = repr(no_eval_native_concat(item))

                    if frame.buffer is None:
                        self.writeline("yield " + val)
                    else:
                        self.writeline(val + ",")
                else:
                    if frame.buffer is None:
                        self.writeline("yield ", item)
                    else:
                        self.newline(item)

                    close = 0

                    if finalize is not None:
                        self.write("environment.finalize(")

                        if finalize_context:
                            self.write("context, ")

                        close += 1

                    self.visit(item, frame)

                    if close > 0:
                        self.write(")" * close)

                    if frame.buffer is not None:
                        self.write(",")

            if frame.buffer is not None:
                # close the open parentheses
                self.outdent()
                self.writeline(len(body) == 1 and ")" or "))")

        # otherwise we create a format string as this is faster in that case
        else:
            format = []
            arguments = []

            for item in body:
                if isinstance(item, list):
                    format.append(
                        no_eval_native_concat(item).replace("%", "%%")
                    )
                else:
                    format.append("%s")
                    arguments.append(item)

            self.writeline("yield ")
            self.write(repr(concat(format)) + " % (")
            self.indent()

            for argument in arguments:
                self.newline(argument)
                close = 0

                if finalize is not None:
                    self.write("environment.finalize(")

                    if finalize_context:
                        self.write("context, ")
                    elif finalize_eval:
                        self.write("context.eval_ctx, ")
                    elif finalize_env:
                        self.write("environment, ")

                    close += 1

                self.visit(argument, frame)
                self.write(")" * close + ", ")

            self.outdent()
            self.writeline(")")

        if outdent_later:
            self.outdent()


class CustomNativeTemplate(Template):
    def render(self, *args, **kwargs):
        """Render the template to produce a native Python type. If the result
        is a single node, its value is returned. Otherwise, the nodes are
        concatenated as strings. If the result can be parsed with
        :func:`ast.literal_eval`, the parsed value is returned. Otherwise, the
        string is returned.
        """
        vars = dict(*args, **kwargs)

        try:
            return no_eval_native_concat(
                self.root_render_func(self.new_context(vars))
            )
        except Exception:
            return self.environment.handle_exception()

    async def render_async(self, *args, **kwargs):
        """Render the template to produce a native Python type. If the result
        is a single node, its value is returned. Otherwise, the nodes are
        concatenated as strings. If the result can be parsed with
        :func:`ast.literal_eval`, the parsed value is returned. Otherwise, the
        string is returned.
        """
        if not self.environment.is_async:
            raise RuntimeError(
                "The environment was not created with async mode " "enabled."
            )

        vars = dict(*args, **kwargs)

        try:
            return await no_eval_native_concat_async(
                self.root_render_func(self.new_context(vars))
            )
        except Exception:
            return self.environment.handle_exception()


class CustomNativeEnvironment(Environment):
    code_generator_class = CustomNativeCodeGenerator
    template_class = CustomNativeTemplate

    def handle_exception(self, source=None):
        # disable template-origin tracebacks because we don't use them anyways
        # TODO provide and use well-formatted, correct template tracebacks
        _, exc_value, _ = sys.exc_info()
        raise exc_value


jinja2_options = dict(
    variable_start_string="(@",
    variable_end_string=")",
    block_start_string="(%",
    block_end_string="%)",
    undefined=StrictUndefined,
    keep_trailing_newline=True,
    extensions=["jinja2.ext.i18n"],
    enable_async=True,
)

environment = CustomNativeEnvironment(
    **{**jinja2_options, "enable_async": False}
)
environment.install_gettext_callables(
    gettext=lambda message: gettext(message.strip()),
    ngettext=lambda singular, plural, n: ngettext(
        singular.strip(), plural.strip(), n
    ),
    newstyle=True,
)

environment_async = CustomNativeEnvironment(**jinja2_options)
environment_async.install_gettext_callables(
    gettext=lambda message: gettext(message.strip()),
    ngettext=lambda singular, plural, n: ngettext(
        singular.strip(), plural.strip(), n
    ),
    newstyle=True,
)


def to_template(obj: str) -> CustomNativeTemplate:
    warnings.warn(
        "Use `to_template_async` instead of `to_template`", DeprecationWarning
    )
    return environment.from_string(obj, template_class=CustomNativeTemplate)


def from_template(context: dict, obj: CustomNativeTemplate) -> Any:
    warnings.warn(
        "Use `from_template_async` instead of `from_template`",
        DeprecationWarning,
    )
    result = obj.render(context)
    if isinstance(result, StrictUndefined):
        result._fail_with_undefined_error()
    else:
        return result


def to_template_async(obj: str) -> CustomNativeTemplate:
    return environment_async.from_string(
        obj, template_class=CustomNativeTemplate
    )


async def from_template_async(context: dict, obj: CustomNativeTemplate) -> Any:
    result = await obj.render_async(context)
    if isinstance(result, StrictUndefined):
        result._fail_with_undefined_error()
    else:
        return result


class TemplateError(Exception):
    def __init__(self, message, lineno, template):
        self.message = message
        self.lineno = lineno
        self.template = template

    def __str__(self):
        lines = self.template.splitlines()
        try:
            line = lines[self.lineno - 1]
            return f"Line {self.lineno} '...{line}...': {self.message}"
        except IndexError:
            return f"Line {self.lineno}: {self.message}"


async def render_dict(
    context: Dict[str, Any], data: Dict[str, Any]
) -> Dict[str, Any]:
    rendered_data = {}

    for key, value in data.items():
        key = await render_value(context, key)
        if isinstance(value, dict):
            rendered_data[key] = await render_dict(context, value)
        elif isinstance(value, list):
            rendered_data[key] = await render_list(context, value)
        else:
            rendered_data[key] = await render_value(context, value)

    return rendered_data


async def render_list(context: Dict[str, Any], data: list) -> list:
    rendered_data = []
    for index, value in enumerate(data):
        if isinstance(value, dict):
            rendered_data.append(await render_dict(context, value))
        elif isinstance(value, list):
            rendered_data.append(await render_list(context, value))
        else:
            rendered_data.append(await render_value(context, value))
    return rendered_data


async def render_value(context: Dict[str, Any], value: Any) -> Any:
    if isinstance(value, str):
        try:
            template = to_template_async(value)
            return await from_template_async(context, template)
        except (
            TemplateSyntaxError,
            MissingUndefinedError,
            UndefinedError,
        ) as error:
            raise TemplateError(
                message=error.message,
                lineno=error.lineno,
                template=value,
            )
    return value
