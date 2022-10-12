import pytest

from meya.entry import Entry
from meya.google.dialogflow.element.mixin import DialogflowContext
from meya.google.dialogflow.element.mixin import DialogflowMixin
from meya.google.dialogflow.integration import DialogflowIntegrationRef
from typing import List
from typing import Optional


class DialogflowElement(DialogflowMixin):
    def process(self) -> List[Entry]:
        pass


@pytest.mark.parametrize(
    ("integration",),
    [(DialogflowIntegrationRef(ref="integration.dialogflow"),)],
)
@pytest.mark.parametrize(("language",), [("en",)])
@pytest.mark.parametrize(
    ("kwargs", "contexts"),
    [
        ({"intent": "intent_0"}, [DialogflowContext(context_id="intent_0")]),
        (
            {"intent": ["intent_0", "intent_1"]},
            [
                DialogflowContext(context_id="intent_0"),
                DialogflowContext(context_id="intent_1"),
            ],
        ),
        (
            {"intent": "intent_0", "input_context": "general"},
            [DialogflowContext(context_id="general")],
        ),
        (
            {
                "intent": "intent_0",
                "input_context": ["context_0", "context_1"],
            },
            [
                DialogflowContext(context_id="context_0"),
                DialogflowContext(context_id="context_1"),
            ],
        ),
        ({"intent": "intent_0", "input_context": False}, None),
        ({"intent": "intent_0", "input_context": None}, []),
        (
            {
                "intent": "intent_0",
                "input_context": [
                    DialogflowContext(
                        context_id="context_0", parameters={"key0": "value0"}
                    )
                ],
            },
            [
                DialogflowContext(
                    context_id="context_0", parameters={"key0": "value0"}
                )
            ],
        ),
        ({"intent_regex": "intent_.*"}, []),
        (
            {"intent_regex": "intent_.*", "input_context": "general"},
            [DialogflowContext(context_id="general")],
        ),
        (
            {
                "intent_regex": "intent_.*",
                "input_context": ["context_0", "context_1"],
            },
            [
                DialogflowContext(context_id="context_0"),
                DialogflowContext(context_id="context_1"),
            ],
        ),
        ({"intent_regex": "intent_.*", "input_context": False}, None),
        ({"intent_regex": "intent_.*", "input_context": None}, []),
        (
            {
                "intent_regex": "intent_.*",
                "input_context": [
                    DialogflowContext(
                        context_id="context_0", parameters={"key0": "value0"}
                    )
                ],
            },
            [
                DialogflowContext(
                    context_id="context_0", parameters={"key0": "value0"}
                )
            ],
        ),
    ],
)
def test_dialogflow_element(
    integration: DialogflowIntegrationRef,
    language: str,
    kwargs: dict,
    contexts: Optional[List[DialogflowElement]],
):
    kwargs.update(integration=integration, language=language)
    element = DialogflowElement(**kwargs)
    if contexts is None:
        assert element.contexts is None
    else:
        assert element.contexts == contexts
