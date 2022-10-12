import pytest

from contextlib import ExitStack
from meya.app_config import AppConfig
from meya.app_vault import AppVault
from meya.core.context import create_load_context
from meya.core.source import Source
from meya.core.source_location import SourceLocation
from meya.core.source_registry import SourceRegistry
from meya.core.template_registry import TemplateRegistry
from meya.element.element_error import ElementParseError
from meya.util.template import CustomNativeTemplate
from typing import Optional
from unittest.mock import MagicMock


async def _parse_and_try_render(
    *sources: Source, app_config: Optional[AppConfig] = None
):
    with ExitStack() as stack:
        app_config = app_config or MagicMock()
        stack.enter_context(AppConfig.current.set(app_config))
        app_vault = MagicMock()
        stack.enter_context(AppVault.current.set(app_vault))
        source_registry = SourceRegistry(list(sources))
        stack.enter_context(SourceRegistry.current.set(source_registry))
        context = create_load_context()
        return await TemplateRegistry.parse_and_try_render(context)


@pytest.mark.asyncio
async def test_ok():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n"
            "steps:\n"
            "  - say: Hi, how are you?\n"
            "  - end\n",
        ),
        Source(
            "trigger/b.yaml",
            "id: trigger.b.go\n"
            "keyword: go\n"
            "action:\n"
            "  flow: a\n"
            "---\n"
            "id: trigger.b.stop\n"
            "regex: stop\n"
            "action: flow.b\n",
        ),
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content == {
        "type": "flow",
        "steps": [{"say": "Hi, how are you?"}, "end"],
    }

    assert template_registry.items[1].source_location == SourceLocation(
        "trigger/b.yaml", 0, 0
    )
    assert not template_registry.items[1].single_document
    assert template_registry.items[1].content == {
        "id": "trigger.b.go",
        "keyword": "go",
        "action": {"flow": "a"},
    }

    assert template_registry.items[2].source_location == SourceLocation(
        "trigger/b.yaml", 5, 0
    )
    assert not template_registry.items[2].single_document
    assert template_registry.items[2].content == {
        "id": "trigger.b.stop",
        "regex": "stop",
        "action": "flow.b",
    }


@pytest.mark.asyncio
async def test_valid_config_ok():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n" "steps:\n" "  - say: (@ config.valid )\n",
        ),
        app_config=AppConfig(valid="VALID"),
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content == {
        "type": "flow",
        "steps": [{"say": "VALID"}],
    }


@pytest.mark.asyncio
async def test_missing_ok():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n" "steps:\n" "  - say: Hi, (@ flow.name )\n",
        )
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content["type"] == "flow"
    assert isinstance(
        template_registry.items[0].content["steps"][0]["say"],
        CustomNativeTemplate,
    )


@pytest.mark.asyncio
async def test_general_render_error():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml", "type: flow\n" "steps:\n" "  - say: (@ 1 / 0 )\n"
        )
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content["type"] == "flow"
    assert (
        repr(template_registry.items[0].content["steps"][0]["say"])
        == "TemplateRegistryRenderError(error=ZeroDivisionError('division by zero'))"
    )


@pytest.mark.asyncio
async def test_missing_config_render_error():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n" "steps:\n" "  - say: (@ config.missing )\n",
        ),
        app_config=AppConfig(valid="VALID"),
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content["type"] == "flow"
    assert (
        repr(template_registry.items[0].content["steps"][0]["say"])
        == """TemplateRegistryRenderError(error=UndefinedError("'meya.app_config.AppConfig object' has no attribute 'missing'"))"""
    )


@pytest.mark.asyncio
async def test_missing_config_render_key_error():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n"
            "steps:\n"
            "  - flow_set:\n"
            "      (@ config.missing ): new\n",
        ),
        app_config=AppConfig(valid="VALID"),
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content["type"] == "flow"
    assert (
        repr(
            list(
                template_registry.items[0]
                .content["steps"][0]["flow_set"]
                .keys()
            )[0]
        )
        == """TemplateRegistryRenderError(error=UndefinedError("'meya.app_config.AppConfig object' has no attribute 'missing'"))"""
    )
    assert (
        list(
            template_registry.items[0].content["steps"][0]["flow_set"].values()
        )[0]
        == "new"
    )


@pytest.mark.asyncio
async def test_missing_nested_config_render_error():
    template_registry = await _parse_and_try_render(
        Source(
            "flow/a.yaml",
            "type: flow\n" "steps:\n" "  - say: (@ config.valid.missing )\n",
        ),
        app_config=AppConfig(valid=dict(nested_valid="VALID")),
    )

    assert template_registry.items[0].source_location == SourceLocation(
        "flow/a.yaml", 0, 0
    )
    assert template_registry.items[0].single_document
    assert template_registry.items[0].content["type"] == "flow"
    assert (
        repr(template_registry.items[0].content["steps"][0]["say"])
        == """TemplateRegistryRenderError(error=UndefinedError("'dict object' has no attribute 'missing'"))"""
    )


@pytest.mark.asyncio
async def test_yaml_simple_scanner_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(Source("flow/a.yaml", "["))
    assert str(excinfo.value) == (
        "expected the node content, but found '<stream end>'\n"
        '  File: "flow/a.yaml", line 1\n'
        "  [\n"
        "   ^"
    )


@pytest.mark.asyncio
async def test_yaml_past_end_scanner_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(
            Source("flow/a.yaml", "steps:\n  - (label): continue\n    end\n")
        )
    assert str(excinfo.value) == (
        "could not find expected ':'\n"
        '  File: "flow/a.yaml", line 4\n'
        "  \n"
        "  ^"
    )


@pytest.mark.asyncio
async def test_yaml_parser_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(Source("flow/a.yaml", "[1, 2"))
    assert str(excinfo.value) == (
        "expected ',' or ']', but got '<stream end>'\n"
        '  File: "flow/a.yaml", line 1\n'
        "  [1, 2\n"
        "       ^"
    )


@pytest.mark.asyncio
async def test_yaml_dict_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(
            Source("flow/a.yaml", "id: i\n" "x: y\n" "---\n" "- item")
        )
    assert str(excinfo.value) == (
        "not a YAML mapping\n"
        '  File: "flow/a.yaml", line 4\n'
        "  - item\n"
        "  ^"
    )


@pytest.mark.asyncio
async def test_jinja2_single_line_parse_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(
            Source(
                "flow/a.yaml",
                "# invalid template\n"
                "type: meya.text.component.say\n"
                "say: (@ flow.name @)\n",
            )
        )
    assert str(excinfo.value) == (
        "unexpected char '@' at 13\n"
        '  File: "flow/a.yaml", line 3\n'
        "  say: (@ flow.name @)"
    )


@pytest.mark.asyncio
async def test_jinja2_multi_line_parse_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(
            Source(
                "flow/a.yaml",
                "# invalid template\n"
                "type: meya.text.component.say\n"
                "say:\n"
                "  Hi \n"
                "  (@ flow.name",
            )
        )
    # YAML merges lines, so jinja2 doesn't see the newline
    assert str(excinfo.value) == (
        "unexpected end of template, expected 'end of print statement'.\n"
        '  File: "flow/a.yaml", line 4\n'
        "    Hi "
    )


@pytest.mark.asyncio
async def test_jinja2_nested_parse_error():
    with pytest.raises(ElementParseError) as excinfo:
        await _parse_and_try_render(
            Source(
                "flow/a.yaml",
                "# invalid template\n"
                "type: meya.component.flow_set\n"
                "flow_set:\n"
                "  job: (@ flow.result )\n"
                "  full_name:\n"
                "    (@ flow.first_name) \n"
                "    (@ flow.last_name",
            )
        )
    # YAML merges lines, so jinja2 doesn't see the newline
    assert str(excinfo.value) == (
        "unexpected end of template, expected 'end of print statement'.\n"
        '  File: "flow/a.yaml", line 6\n'
        "      (@ flow.first_name) "
    )
