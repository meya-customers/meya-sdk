import math
import pytest

from console.k8s.gcp import ServiceAccount
from dataclasses import MISSING
from dataclasses import dataclass
from datetime import timedelta
from meya.app_vault import AppVault
from meya.bot.element import Bot
from meya.button.component.ask import ButtonAskComponent
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonType
from meya.component.spec import ActionComponentSpec
from meya.component.spec import ComponentSpec
from meya.component.spec import FlowComponentSpec
from meya.core.source_location import SourceLocation
from meya.db.view.thread import ThreadMode
from meya.element.element_test import to_spec
from meya.email.component.address.ask.form import EmailAddressAskFormComponent
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerVisibility
from meya.flow.component.if_ import IfComponent
from meya.flow.element import Flow
from meya.flow.element import FlowRef
from meya.flow.element import StepLabel
from meya.freshworks.freshchat.integration import FreshchatAssignmentRules
from meya.orb.component.magic_link import OrbMagicLinkComponent
from meya.orb.integration import OrbIntegrationRef
from meya.sensitive_data import SensitiveDataRef
from meya.session.trigger.chat.open import ChatOpenTrigger
from meya.text.component.ask import AskComponent
from meya.text.component.say import SayComponent
from meya.util.dict import from_dict
from meya.util.dict import merge_dicts
from meya.util.dict import to_dict
from meya.util.msgpack import from_msgpack
from meya.util.msgpack import to_msgpack
from meya_private.zendesk.chat.payload.start import ZendeskChatStartResponse
from typing import Any
from typing import Optional


@pytest.mark.parametrize(
    ("obj", "dict_obj"),
    [
        (Bot(), {}),
        (EmailAddressAskFormComponent(), {}),
        (AskComponent(ask="?"), {"ask": "?", "quick_replies": MISSING}),
        (
            ComponentSpec(
                type="demo.component.data_2",
                data={"data_2": 2},
                id=None,
                source_location=SourceLocation(
                    file_path="flow/data.yaml", line=16, column=4
                ),
            ),
            {
                "type": "demo.component.data_2",
                "data": {"data_1": MISSING, "data_2": 2},
                "id": None,
                "source_location": {
                    "file_path": "flow/data.yaml",
                    "line": 16,
                    "column": 4,
                },
            },
        ),
        (
            ButtonAskComponent(buttons=["a", "b"]),
            {"buttons": ["a", MISSING, "b"]},
        ),
    ],
)
def test_from_dict(obj: Any, dict_obj: Any):
    assert from_dict(type(obj), dict_obj) == obj


@dataclass
class Brand:
    name: str
    company: Optional[str]


@dataclass
class Ball:
    name: str
    color: Optional[str]
    brand: Brand


@pytest.mark.parametrize(
    ("obj", "dict_obj", "preserve_nones"),
    [
        (
            ButtonElementSpec(text="b1", result=MISSING),
            {"text": "b1", "context": {}},
            None,
        ),
        ({"k1": "v1", "k2": MISSING}, {"k1": "v1"}, None),
        ([1, 2, MISSING, 4], [1, 2, 4], None),
        (MISSING, MISSING, None),
        ({"a": 1, "b": None}, {"a": 1, "b": None}, False),
        ({"a": 1, "b": None}, {"a": 1, "b": None}, True),
        (
            Ball(
                name="basketball",
                color=None,
                brand=Brand(name="Wilson", company=None),
            ),
            {"name": "basketball", "brand": {"name": "Wilson"}},
            False,
        ),
        (
            Ball(
                name="basketball",
                color=None,
                brand=Brand(name="Wilson", company=None),
            ),
            {
                "name": "basketball",
                "color": None,
                "brand": {"name": "Wilson", "company": None},
            },
            True,
        ),
    ],
)
def test_to_dict(obj: Any, dict_obj: Any, preserve_nones: bool):
    if preserve_nones is None:
        assert to_dict(obj) == dict_obj
    else:
        assert to_dict(obj, preserve_nones=preserve_nones) == dict_obj


@pytest.mark.parametrize(
    ("obj", "dict_obj", "camel_case_fields"),
    [
        ({"x": 1}, {"x": 1}, False),
        ({3}, [3], False),
        (timedelta(days=2, milliseconds=9), "2d 9ms", False),
        (1.0, 1.0, False),
        (math.inf, "inf", False),
        (-math.inf, "-inf", False),
        (FlowRef("f1"), {"ref": "f1"}, False),
        (
            Flow(
                steps=[
                    StepLabel("start"),
                    to_spec(SayComponent(say="hi"), FlowComponentSpec),
                ]
            ),
            {
                "steps": [
                    {"step_label": "start"},
                    {
                        "data": {
                            "composer": {},
                            "context": {},
                            "say": "hi",
                            "quick_replies": [],
                            "header": {},
                            "sensitive": False,
                            "triggers": [],
                        },
                        "type": "meya.text.component.say",
                    },
                ],
                "triggers": [],
            },
            False,
        ),
        (
            SayComponent(
                say="hi",
                composer=ComposerElementSpec(
                    visibility=ComposerVisibility.HIDE, placeholder="here"
                ),
            ),
            {
                "composer": {"placeholder": "here", "visibility": "hide"},
                "context": {},
                "say": "hi",
                "quick_replies": [],
                "header": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            ButtonAskComponent(
                buttons=[
                    ButtonElementSpec(text="b1", result="r"),
                    ButtonElementSpec(
                        text="b1", result="r", type=ButtonType.COMPONENT_NEXT
                    ),
                    ButtonElementSpec(text="b2", result=None),
                    ButtonElementSpec(text="b3"),
                ]
            ),
            {
                "buttons": [
                    {"text": "b1", "result": "r", "context": {}},
                    {
                        "text": "b1",
                        "result": "r",
                        "type": "component_next",
                        "context": {},
                    },
                    {"text": "b2", "result": None, "context": {}},
                    {"text": "b3", "context": {}},
                ],
                "composer": {"focus": "blur"},
                "context": {},
                "error_message": "Please select an option",
                "multi": False,
                "quick_replies": [],
                "header": {},
                "required": False,
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            IfComponent(
                if_=None,
                then=ActionComponentSpec(
                    type="meya.component.control.jump",
                    data={
                        "jump": {"ref": "ok"},
                        "context_flow": {"ref": "flow"},
                    },
                    id=None,
                    source_location=None,
                ),
                else_=ActionComponentSpec(
                    type="meya.component.control.jump",
                    data={
                        "jump": {"ref": "not_ok"},
                        "context_flow": {"ref": "flow"},
                    },
                    id=None,
                    source_location=None,
                ),
            ),
            {
                "then": {
                    "type": "meya.component.control.jump",
                    "data": {
                        "jump": {"ref": "ok"},
                        "context_flow": {"ref": "flow"},
                    },
                },
                "else_": {
                    "type": "meya.component.control.jump",
                    "data": {
                        "jump": {"ref": "not_ok"},
                        "context_flow": {"ref": "flow"},
                    },
                },
                "context": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            EmailAddressAskFormComponent(label="Your email", placeholder=None),
            {
                "autocomplete": "email",
                "composer": {"focus": "blur"},
                "context": {},
                "error_message": "Invalid email",
                "field_name": "email",
                "label": "Your email",
                "placeholder": None,
                "retries": "inf",
                "quick_replies": [],
                "header": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            SayComponent(say=None),
            {
                "composer": {},
                "context": {},
                "quick_replies": [],
                "header": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            ChatOpenTrigger(
                when=True,
                action=ActionComponentSpec(
                    type="demo.component.data_2",
                    data=None,
                    id=None,
                    source_location=SourceLocation(
                        file_path="flow/data.yaml", line=16, column=4
                    ),
                ),
            ),
            {
                "when": True,
                "action": {
                    "source_location": {
                        "column": 4,
                        "file_path": "flow/data.yaml",
                        "line": 16,
                    },
                    "type": "demo.component.data_2",
                },
            },
            False,
        ),
        (
            ChatOpenTrigger(
                when=None,
                action=ActionComponentSpec(
                    type="demo.component.data_2",
                    data=None,
                    id=None,
                    source_location=SourceLocation(
                        file_path="flow/data.yaml", line=16, column=4
                    ),
                ),
            ),
            {
                "when": None,
                "action": {
                    "source_location": {
                        "column": 4,
                        "file_path": "flow/data.yaml",
                        "line": 16,
                    },
                    "type": "demo.component.data_2",
                },
            },
            False,
        ),
        (
            ChatOpenTrigger(
                action=ActionComponentSpec(
                    type="demo.component.data_2",
                    data=None,
                    id=None,
                    source_location=SourceLocation(
                        file_path="flow/data.yaml", line=16, column=4
                    ),
                )
            ),
            {
                "action": {
                    "source_location": {
                        "column": 4,
                        "file_path": "flow/data.yaml",
                        "line": 16,
                    },
                    "type": "demo.component.data_2",
                }
            },
            False,
        ),
        (
            OrbMagicLinkComponent(
                integration=OrbIntegrationRef("orb.default"),
                magic_link="https://example.org",
                button_id=True,
                single_use=True,
                expiry=timedelta(minutes=20, seconds=6),
            ),
            {
                "button_id": True,
                "expiry": "20m 6s",
                "integration": {"ref": "orb.default"},
                "magic_link": "https://example.org",
                "single_use": True,
                "context": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            OrbMagicLinkComponent(
                integration=OrbIntegrationRef("orb.default"),
                magic_link="https://example.org",
                button_id="b-1",
                single_use=False,
            ),
            {
                "button_id": "b-1",
                "expiry": "1d",
                "integration": {"ref": "orb.default"},
                "magic_link": "https://example.org",
                "single_use": False,
                "context": {},
                "sensitive": False,
                "triggers": [],
            },
            False,
        ),
        (
            ServiceAccount(
                configuration=None,
                project_id="abc",
                region=None,
                email="test@meya.ai",
                key={"secret": "xyz"},
            ),
            {
                "email": "test@meya.ai",
                "key": {"secret": "xyz"},
                "project_id": "abc",
            },
            False,
        ),
        (AppVault(), {}, False),
        (
            ComponentSpec(
                type="demo.component.data_2",
                data=None,
                id=None,
                source_location=SourceLocation(
                    file_path="flow/data.yaml", line=16, column=4
                ),
            ),
            {
                "type": "demo.component.data_2",
                "source_location": {
                    "file_path": "flow/data.yaml",
                    "line": 16,
                    "column": 4,
                },
            },
            False,
        ),
        (
            FreshchatAssignmentRules(
                human_agent=ThreadMode("expert"), group=ThreadMode.BOT
            ),
            {
                "bot_agent": "bot",
                "group": "bot",
                "human_agent": "expert",
                "no_assignee": "bot",
            },
            False,
        ),
        (
            ZendeskChatStartResponse(ok=True, z_user_id="u1", z_cookie="c2"),
            {"ok": True, "zCookie": "c2", "zUserId": "u1"},
            True,
        ),
        (SensitiveDataRef("xyz"), {"🔐🙈": "xyz"}, False),
    ],
)
def test_round_trip(obj: Any, dict_obj: Any, camel_case_fields: bool):
    assert to_dict(obj, to_camel_case_fields=camel_case_fields) == dict_obj
    assert (
        from_dict(
            type(obj), dict_obj, from_camel_case_fields=camel_case_fields
        )
        == obj
    )

    result = from_dict(
        type(obj),
        to_dict(obj, to_camel_case_fields=camel_case_fields),
        from_camel_case_fields=camel_case_fields,
    )
    assert result == obj
    result = from_dict(
        type(obj),
        from_msgpack(
            to_msgpack(to_dict(obj, to_camel_case_fields=camel_case_fields))
        ),
        from_camel_case_fields=camel_case_fields,
    )
    assert result == obj

    result = to_dict(
        from_dict(
            type(obj), dict_obj, from_camel_case_fields=camel_case_fields
        ),
        to_camel_case_fields=camel_case_fields,
    )
    assert result == dict_obj
    result = to_dict(
        from_dict(
            type(obj),
            from_msgpack(to_msgpack(dict_obj)),
            from_camel_case_fields=camel_case_fields,
        ),
        to_camel_case_fields=camel_case_fields,
    )
    assert result == dict_obj


def test_to_str_subclass():
    mode = to_dict(ThreadMode.BOT)
    assert type(mode) is str


def test_from_str_subclass():
    mode = from_dict(ThreadMode, "bot")
    assert type(mode) is ThreadMode


def test_nan():
    assert to_dict(math.nan) == "nan"
    assert math.isnan(from_dict(float, "nan"))


def test_merge_dicts():
    d1 = {"a": {"c": 4, "d": {"e": 2}}, "b": 2}
    d2 = {"a": {"d": {"e": 6}}, "b": 3, "c": 4}
    assert merge_dicts(d1, d2) == {
        "a": {"c": 4, "d": {"e": 6}},
        "b": 3,
        "c": 4,
    }
