import pytest

from meya.util.yaml import from_yaml
from meya.util.yaml import to_yaml


@pytest.mark.parametrize(
    ("text", "obj"),
    [
        ("  - 1\n  - 2\n  - 3\n", [1, 2, 3]),
        (
            "sendgrid_email_address: test🤯@sendgrid.meya.ai\n",
            {"sendgrid_email_address": "test🤯@sendgrid.meya.ai"},
        ),
        (
            "say0:\nsay1: ''\nsay2: ' '\n",
            {"say0": None, "say1": "", "say2": " "},
        ),
        (
            "  - type: parallel\n"
            "    steps:\n"
            "      - name: check\n"
            "        service: meya-grid\n"
            "        command: v2 check\n"
            "      - name: test\n"
            "        service: meya-grid\n"
            "        command: v2 test --nowatch\n",
            [
                {
                    "type": "parallel",
                    "steps": [
                        {
                            "name": "check",
                            "service": "meya-grid",
                            "command": "v2 check",
                        },
                        {
                            "name": "test",
                            "service": "meya-grid",
                            "command": "v2 test --nowatch",
                        },
                    ],
                }
            ],
        ),
        (
            "initContainers:\n"
            "  - args:\n"
            "      - /mnt/config/checkout.py\n"
            "      - 1e09ca5a8a32b4a\n"
            "      - 1e09ca5a8a32b4a\n"
            "      - no\n"
            "      - ''\n"
            "    command:\n"
            "      - python3\n",
            {
                "initContainers": [
                    {
                        "args": [
                            "/mnt/config/checkout.py",
                            "1e09ca5a8a32b4a",
                            "1e09ca5a8a32b4a",
                            "no",
                            "",
                        ],
                        "command": ["python3"],
                    }
                ]
            },
        ),
    ],
)
def test_load_and_dump(text, obj):
    assert from_yaml(text) == obj
    assert to_yaml(obj) == text


def test_load_multiline():
    text = (
        "consistent_indent: >\n"
        "  abc\n"
        "  def\n"
        "  ghi\n"
        "extra_indent: >\n"
        "  abc\n"
        "  123\n"
        "    def\n"
        "    456\n"
        "  ghi\n"
        "  789\n"
        "explicit_indent: >2\n"
        "    abc\n"
        "      def\n"
        "    ghi\n"
    )
    obj = {
        "consistent_indent": "abc def ghi\n",
        "extra_indent": "abc 123\n  def\n  456\nghi 789\n",
        "explicit_indent": "  abc\n    def\n  ghi\n",
    }
    assert from_yaml(text) == obj


def test_round_trip_modify():
    obj = from_yaml(
        "# This is my file\n"
        "a_key: 1\n"
        "\n"
        "some_key: two\n"
        "another key: [3] # With a comment\n"
    )
    obj["new_key"] = "NEW"
    obj["a_key"] = 5
    assert to_yaml(obj) == (
        "# This is my file\n"
        "a_key: 5\n"
        "\n"
        "some_key: two\n"
        "another key: [3] # With a comment\n"
        "new_key: NEW\n"
    )


def test_autoformat():
    obj = from_yaml(
        "a123:\n"
        "      b456: c789 # f000\n"
        "# g1111111\n"
        "d2222:\n"
        "    -   e\n"
        "null0: null\n"
        "null1: ~\n"
        "null2: \n"
    )
    assert to_yaml(obj) == (
        "a123:\n"
        "  b456: c789     # f000\n"
        "# g1111111\n"
        "d2222:\n"
        "  - e\n"
        "null0:\n"
        "null1:\n"
        "null2:\n"
    )
