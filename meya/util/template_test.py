import asyncio
import pytest

from dataclasses import dataclass
from meya.util.template import from_template_async
from meya.util.template import to_template_async
from meya.util.undefined import MISSING_UNDEFINED


@pytest.mark.parametrize(
    ("text", "expected_result"),
    [
        # String constants
        ("5", "5"),
        ("", ""),
        (" ", " "),
        ("[1, 2, 3]", "[1, 2, 3]"),
        # Constant expressions
        ("( (@ 1 ) + (@ 2 ) )", "( 1 + 2 )"),
        ("(@ 1 + (2 * 3) )", 7),
        ("(@ '6' )", "6"),
        ("(@ '' )", ""),
        ("(@ ' ' )", " "),
        ("(@ none )", None),
        # Control flow
        ("(% for x in ['a', 'b'] %)(@ x )+(% endfor %)", "a+b+"),
        ("(% if true %)Y(% else %)N(% endif %)", "Y"),
        ("(% if false %)Y(% else %)N(% endif %)", "N"),
        # Dict operations
        ("(@ flow.custom_dict )", {"c": 1.2, "d": True}),
        ("(@ flow.custom_dict )x", "{'c': 1.2, 'd': True}x"),
        ("x(@ flow.custom_dict )", "x{'c': 1.2, 'd': True}"),
        ("(@ flow.custom_dict ) ", "{'c': 1.2, 'd': True} "),
        (" (@ flow.custom_dict )", " {'c': 1.2, 'd': True}"),
        ("(@ flow.custom_dict.c )", 1.2),
        ("(@ flow.custom_dict.c | upper )", "1.2"),
        ("(@ flow.custom_dict.bogus | default(10) )", 10),
        ("(@ flow.custom_dict.keys() | map('upper') | list )", ["C", "D"]),
        ("(@ flow.custom_dict.values() | select('gt', 1) | list )", [1.2]),
        # String operations
        ("(@ flow.custom_str )", "[4, 5, 6]"),
        ("(@ flow.custom_str | int )", 0),
        ("(@ flow.custom_str is equalto('y') )", False),
        ("(@ flow.custom_str[:4] )", "[4, "),
        ("(@ flow.custom_str[2:] )", ", 5, 6]"),
        ("(@ flow.custom_str[1:3] )", "4,"),
        ("(@ flow.custom_str[7] )", "6"),
        ("(@ flow.custom_str[-5] )", "5"),
        # List operations
        ("(@ flow.custom_list )", [100, 101, 102, 103, 104]),
        ("(@ flow.custom_list[:3] )", [100, 101, 102]),
        ("(@ flow.custom_list[3:] )", [103, 104]),
        ("(@ flow.custom_list[2:4] )", [102, 103]),
        ("(@ flow.custom_list[3] )", 103),
        ("(@ flow.custom_list[-3] )", 102),
        (
            "(@ flow.custom_list | map('string') | list )",
            ["100", "101", "102", "103", "104"],
        ),
        ("(@ flow.custom_list | select('even') | join('-') )", "100-102-104"),
        # Async operations
        (
            "(% for x in flow.custom_async_generator() %)(@ x )+(% endfor %)",
            "{'name': 'a'}+{'name': 'b'}+{'name': 'c'}+",
        ),
        (
            "(@ flow.custom_async_method.query() | map(attribute='name') | join(',') )",
            "d,e,f",
        ),
        (
            "(@ flow.custom_async_item.x | rejectattr('x', 'lt', 'h') | list )",
            [{"x": "h"}, {"x": "i"}],
        ),
        ("(@ flow.custom_async_item['y'][:2] )", [{"y": "g"}, {"y": "h"}]),
        # Errors
        (
            "(@ flow.custom_dict.c.bogus )",
            "UndefinedError(\"'float object' has no attribute 'bogus'\")",
        ),
        (
            "(@ flow.custom_dict and flow.custom_dict.bogus )",
            "UndefinedError(\"'dict object' has no attribute 'bogus'\")",
        ),
        (
            "(@ flow.custom_str > 0 )",
            "TypeError(\"'>' not supported between instances of 'str' and 'int'\")",
        ),
        (
            "(@ flow.custom_undefined )",
            "UndefinedError(\"'dict object' has no attribute 'custom_undefined'\")",
        ),
        (
            "(@ flow.bogus )",
            "UndefinedError(\"'dict object' has no attribute 'bogus'\")",
        ),
        ('(@ flow.get("bogus") )', None),
        ("(@ flow.bogus | default(3) )", 3),
        (
            "(@ flow.bogus | int )",
            "UndefinedError(\"'dict object' has no attribute 'bogus'\")",
        ),
        (
            "(@ flow.bogus | upper )",
            "UndefinedError(\"'dict object' has no attribute 'bogus'\")",
        ),
        (
            "Bogus (@ flow.bogus )",
            "UndefinedError(\"'dict object' has no attribute 'bogus'\")",
        ),
        (
            "(@ undefined_user )",
            "UndefinedError(\"'undefined_user' is undefined\")",
        ),
        ("(@ missing )", "MissingUndefinedError('None is undefined')"),
        ("(@ missing.abc )", "MissingUndefinedError('None is undefined')"),
    ],
)
@pytest.mark.asyncio
async def test_native_template_async(text, expected_result):
    template = to_template_async(text)
    try:

        async def async_generator():
            yield {"name": "a"}
            await asyncio.sleep(0)
            yield {"name": "b"}
            await asyncio.sleep(0)
            yield {"name": "c"}

        @dataclass
        class AsyncMethod:
            async def query(self):
                await asyncio.sleep(0)
                return [{"name": "d"}, {"name": "e"}, {"name": "f"}]

        @dataclass
        class AsyncItem:
            def __getitem__(self, key):
                return self.get(key)

            async def get(self, key):
                await asyncio.sleep(0)
                return [{key: "g"}, {key: "h"}, {key: "i"}]

        result = await from_template_async(
            dict(
                flow={
                    "custom_dict": {"c": 1.2, "d": True},
                    "custom_str": "[4, 5, 6]",
                    "custom_list": [100, 101, 102, 103, 104],
                    "custom_async_generator": async_generator,
                    "custom_async_method": AsyncMethod(),
                    "custom_async_item": AsyncItem(),
                },
                missing=MISSING_UNDEFINED,
            ),
            template,
        )
    except Exception as e:
        result = repr(e)
    assert result == expected_result
