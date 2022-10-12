import meya
import pytest

from meya.bot.element import Bot
from meya.button.component.ask import ButtonAskComponent
from meya.button.event.click import ButtonClickEvent
from meya.component.element import Component
from meya.core.type_registry import ElementSignature
from meya.core.type_registry import TypeRegistry
from meya.element import Element
from meya.email.component.address.ask import EmailAddressAskComponent
from meya.email.component.address.ask.form import EmailAddressAskFormComponent
from meya.entry import Entry
from meya.file.component import FileComponent
from meya.file.component.ask import FileAskComponent
from meya.flow.component import FlowComponent
from meya.flow.component.end import EndComponent
from meya.flow.component.if_ import IfComponent
from meya.flow.element import Flow
from meya.google.dialogflow.component.ask import DialogflowAskComponent
from meya.google.dialogflow.component.ask.form import (
    DialogflowAskFormComponent,
)
from meya.google.dialogflow.trigger import DialogflowTrigger
from meya.image.component import ImageComponent
from meya.image.component.ask import ImageAskComponent
from meya.sendgrid.integration import SendgridIntegration
from meya.text.component.ask import AskComponent
from meya.text.component.ask.form import AskFormComponent
from meya.text.component.ask_regex import AskRegexComponent
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent
from meya.text.trigger.regex import RegexTrigger
from meya.tile.component.ask import TileAskComponent
from meya.twilio.voice.component.gather import TwilioVoiceGatherComponent
from meya.util.template import to_template_async
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from unittest.mock import MagicMock


@pytest.mark.parametrize(
    ("item_type",),
    [
        (SayComponent,),
        (SendgridIntegration,),
        (SayEvent,),
        (ButtonClickEvent,),
    ],
)
def test_items(item_type: Type[Element]):
    type_registry = TypeRegistry.import_and_index(meya)
    assert item_type in type_registry.items


@pytest.mark.parametrize(
    ("item_alias", "element_extra_alias", "item_type"),
    [
        ("meya.bot.element", None, Bot),
        ("meya.flow.element", None, Flow),
        ("meya.text.component.say", None, SayComponent),
        ("meya.text.component.ask", None, AskComponent),
        ("meya.text.component.ask.form", None, AskFormComponent),
        ("meya.flow.component.if", None, IfComponent),
        ("meya.flow.component.end", "end", EndComponent),
        ("meya.sendgrid.integration", None, SendgridIntegration),
        ("meya.text.event.say", None, SayEvent),
    ],
)
def test_alias(
    item_alias: str, element_extra_alias: str, item_type: Type[Element]
):
    type_registry = TypeRegistry.import_and_index(meya)
    assert item_type in type_registry.items
    assert type_registry.alias[item_alias] is item_type
    if element_extra_alias:
        assert type_registry.alias[element_extra_alias] is item_type
    assert type_registry.reverse_alias[item_type] == item_alias


@pytest.mark.parametrize(("item_alias", "item_type"), [("meya.entry", Entry)])
def test_no_abstract(item_alias: str, item_type: Type):
    type_registry = TypeRegistry.import_and_index(meya)
    assert item_type not in type_registry.items
    assert type_registry.alias.get(item_alias) is None
    assert type_registry.reverse_alias.get(item_type) is None


@pytest.mark.parametrize(
    ("item_alias", "item_type"),
    [("meya.element", Element), ("meya.component.element", Component)],
)
def test_includes_base_classes(item_alias: str, item_type: Type):
    type_registry = TypeRegistry.import_and_index(meya)
    assert item_type in type_registry.items
    assert type_registry.alias.get(item_alias) is item_type
    assert type_registry.reverse_alias.get(item_type) == item_alias


@pytest.mark.parametrize(
    ("content", "item_type"),
    [
        ({"ask": MagicMock()}, AskComponent),
        ({"ask": MagicMock(), "expect": "x"}, AskComponent),
        ({"ask": MagicMock(), "expect": 5}, AskComponent),
        ({"ask_form": MagicMock()}, AskFormComponent),
        ({"ask": MagicMock(), "expect": to_template_async('(@ "x" )')}, None),
        (
            {"ask_form": MagicMock(), "expect": to_template_async('(@ "x" )')},
            None,
        ),
        (
            {"ask": MagicMock(), "expect": "email_address"},
            EmailAddressAskComponent,
        ),
        (
            {"ask_form": MagicMock(), "expect": "email_address"},
            EmailAddressAskFormComponent,
        ),
        ({"ask": MagicMock(), "expect": "dialogflow"}, DialogflowAskComponent),
        (
            {
                "ask": MagicMock(),
                "expect": "dialogflow",
                "integration": MagicMock(),
            },
            DialogflowAskComponent,
        ),
        (
            {"ask_form": MagicMock(), "expect": "dialogflow"},
            DialogflowAskFormComponent,
        ),
        ({"ask": MagicMock(), "regex": MagicMock()}, AskRegexComponent),
        (
            {"ask": MagicMock(), "regex": MagicMock(), "x": MagicMock()},
            AskRegexComponent,
        ),
        ({"regex": MagicMock()}, RegexTrigger),
        ({"ask": MagicMock(), "expect": "file"}, FileAskComponent),
        ({"ask": MagicMock(), "expect": "image"}, ImageAskComponent),
        ({"ask": MagicMock(), "input": "dtmf"}, TwilioVoiceGatherComponent),
        ({"ask": MagicMock(), "buttons": MagicMock()}, ButtonAskComponent),
        (
            {"ask": MagicMock(), "buttons": MagicMock(), "x": MagicMock()},
            ButtonAskComponent,
        ),
        ({"buttons": MagicMock()}, ButtonAskComponent),
        ({"ask": MagicMock(), "tiles": MagicMock()}, TileAskComponent),
        ({"tiles": MagicMock()}, TileAskComponent),
        ({"say": MagicMock()}, SayComponent),
        ({"say": MagicMock(), "x": MagicMock()}, SayComponent),
        ({"sayx": MagicMock()}, None),
        (
            {"if": MagicMock(), "then": MagicMock(), "else": MagicMock()},
            IfComponent,
        ),
        ({"end": MagicMock()}, EndComponent),
        ({"flow": MagicMock(), "jump": MagicMock()}, FlowComponent),
        ({"url": MagicMock()}, None),
        ({"url": MagicMock(), "alt": MagicMock()}, ImageComponent),
        ({"url": MagicMock(), "filename": MagicMock()}, FileComponent),
        (
            {"url": MagicMock(), "filename": MagicMock(), "x": MagicMock()},
            FileComponent,
        ),
        ({"url": MagicMock(), "x": MagicMock()}, None),
        ({"expect": "dialogflow"}, DialogflowTrigger),
    ],
)
def test_signature(
    content: Dict[str, Any], item_type: Optional[Type[Element]]
):
    type_registry = TypeRegistry.import_and_index(meya)
    assert type_registry.match_signature(content) is item_type
    type_registry.signature = list(reversed(type_registry.signature))
    assert type_registry.match_signature(content) is item_type


@pytest.mark.parametrize(
    ("content", "item_type"),
    [
        ({"url": MagicMock()}, None),
        ({"url": MagicMock(), "alt": MagicMock()}, ImageComponent),
        ({"url": MagicMock(), "filename": MagicMock()}, FileComponent),
        (
            {"url": MagicMock(), "filename": MagicMock(), "x": MagicMock()},
            FileComponent,
        ),
        ({"url": MagicMock(), "x": MagicMock()}, None),
    ],
)
def test_ambiguous_signature(
    content: Dict[str, Any], item_type: Optional[Type[Element]]
):
    type_registry = TypeRegistry.import_and_index()
    type_registry.signature = [
        ElementSignature({"url": str}, {"alt"}, ImageComponent),
        ElementSignature({"url": str}, {"filename"}, FileComponent),
    ]
    assert type_registry.match_signature(content) is item_type
    type_registry.signature = list(reversed(type_registry.signature))
    assert type_registry.match_signature(content) is item_type
