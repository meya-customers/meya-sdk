import re

from dataclasses import dataclass
from dataclasses import field
from meya.core.meta_level import MetaLevel
from meya.element import Element
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.google.dialogflow.integration import DialogflowIntegrationRef
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconElementSpecUnion
from meya.text.trigger.regex import RegexTrigger
from numbers import Real
from typing import List
from typing import Optional
from typing import Union

MAX_CONTEXT_ID_LEN: Real = 250


@dataclass
class DialogflowContext:
    context_id: str
    parameters: dict = field(default_factory=dict)


@dataclass
class DialogflowMixin(Element):
    is_abstract: bool = meta_field(value=True)
    meta_icon: IconElementSpecUnion = meta_field(
        value=IconElementSpec(
            url="https://meya-website.cdn.prismic.io/meya-website/175d925e-6a3a-4c27-b13c-04fe955d1a25_dialogflow.svg"
        )
    )

    integration: DialogflowIntegrationRef = element_field(
        level=MetaLevel.INTERMEDIATE,
        help="The reference path to the configured Dialogflow integration.",
    )
    language: Optional[str] = element_field(
        default=None,
        help=(
            "The language code to be used for the Dialogflow API queries. If "
            "this is not provided explicitly, the user's language will be "
            "used. If the user has no language set, it will default to `en`."
        ),
    )
    intent: Optional[Union[str, List[str]]] = element_field(
        default=None,
        level=MetaLevel.BASIC,
        help=(
            "The specific intent (or list of intents) to match if the "
            "confidence exceeds the specified `min_confidence`."
        ),
    )
    intent_regex: Optional[str] = element_field(
        default=None,
        level=MetaLevel.BASIC,
        help=(
            "The regex pattern to match the returned intent against if the "
            "confidence exceeds the specified `min_confidence`."
        ),
    )
    min_confidence: Optional[Real] = element_field(
        default=0.75,
        help=(
            "The minimum confidence threshold that the intent needs to "
            "achieve for the trigger to match."
        ),
    )
    max_confidence: Optional[Real] = element_field(
        default=1.0,
        help=(
            "The maximum confidence threshold that the intent should not "
            "exceed for the trigger to match."
        ),
    )
    input_context: Optional[
        Union[bool, str, List[Union[str, DialogflowContext]]]
    ] = element_field(
        default=True,
        help=(
            "The optional input contexts that need to be applied to the "
            "detect intent API call. Providing an input context will inform "
            "Dialogflow to only evaluate intents that match the specified "
            "input contexts."
        ),
    )

    def validate(self):
        super().validate()
        if isinstance(self.input_context, str):
            contexts = [self.input_context]
        elif isinstance(self.input_context, bool):
            contexts = []
        else:
            contexts = self.input_context or []
        for context in contexts:
            if isinstance(context, DialogflowContext):
                context = context.context_id
            if not re.match("^[-a-zA-Z0-9_%]*$", context):
                raise self.validation_error(
                    f"invalid Dialogflow context id '{context}', "
                    f"the context id may only contain characters in "
                    f"'a-zA-Z0-9_-%'"
                )
            if len(context) > MAX_CONTEXT_ID_LEN:
                raise self.validation_error(
                    f"the Dialogflow context id cannot be longer than "
                    f"{MAX_CONTEXT_ID_LEN} characters"
                )
        if self.intent is not None and self.intent_regex is not None:
            raise self.validation_error(
                "you cannot specify both 'intent' and 'intent_regex' "
                "properties at the same time"
            )

    @property
    def contexts(self) -> Optional[List[DialogflowContext]]:
        if isinstance(self.input_context, bool):
            if not self.input_context:
                return None
            elif self.input_context and isinstance(self.intent, list):
                return [
                    DialogflowContext(context_id=intent)
                    for intent in self.intent
                ]
            elif self.input_context and isinstance(self.intent, str):
                return [DialogflowContext(context_id=self.intent)]
            else:
                return []
        elif isinstance(self.input_context, str):
            return [DialogflowContext(context_id=self.input_context)]
        elif isinstance(self.input_context, list):
            return [
                context
                if isinstance(context, DialogflowContext)
                else DialogflowContext(context_id=context)
                for context in self.input_context
            ]
        else:
            return []

    def set_language(self):
        if self.language is None:
            # TODO Read default language from app config
            self.language = self.user.language or "en"

    def is_match(self, confidence: Real, intent: str) -> bool:
        match = False
        if not self.intent_regex and not self.intent:
            match = True
        elif self.intent_regex and RegexTrigger.search_regex(
            self.intent_regex, intent, ignorecase=True
        ):
            match = True
        elif isinstance(self.intent, str) and self.intent == intent:
            match = True
        elif isinstance(self.intent, list) and intent in self.intent:
            match = True

        return (
            match and self.min_confidence <= confidence <= self.max_confidence
        )
