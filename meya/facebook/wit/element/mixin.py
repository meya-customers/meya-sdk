from dataclasses import dataclass
from meya.core.meta_level import MetaLevel
from meya.element import Element
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.facebook.wit.integration import WitIntegrationRef
from meya.facebook.wit.payload import WitContextCoords
from meya.facebook.wit.payload import WitIntent
from meya.text.trigger.regex import RegexTrigger
from meya.time import Timezone
from numbers import Real
from typing import List
from typing import Optional
from typing import Union


@dataclass
class WitMixin(Element):
    is_abstract: bool = meta_field(value=True)

    integration: WitIntegrationRef = element_field(
        level=MetaLevel.INTERMEDIATE,
        help="The reference path to the configured Dialogflow integration.",
    )
    intent: Union[None, str, List[str]] = element_field(
        default=None,
        help=(
            "The specific intent (or list of intents) to match if the "
            "confidence exceeds the specified `min_confidence`."
        ),
    )
    intent_regex: Optional[str] = element_field(
        default=None,
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
    locale: Optional[str] = element_field(
        default=None,
        help=(
            "The first 2 letters must be a valid ISO639-1 language, followed "
            "by an underscore, followed by a valid ISO3166 alpha2 country "
            "code. Locale is used to resolve the entities."
        ),
    )
    coords: Optional[WitContextCoords] = element_field(
        default=None,
        help=(
            "The user's location coordinates. "
            "Must be in the form of an object with 'lat': float and "
            "'long': float. "
            "This field is used to improve ranking for wit/location's "
            "resolved values."
        ),
    )
    timezone: Optional[Timezone] = element_field(
        default=None,
        help=(
            "Must be a valid IANA timezone. "
            "Used only if no `reference_time` is provided. "
            "Example: 'America/Los_Angeles'"
        ),
    )
    reference_time: Optional[str] = element_field(
        default=None,
        help=(
            "Local date and time of the user in ISO8601 format. "
            "Do not use UTC time."
        ),
    )

    def validate(self):
        super().validate()
        if self.intent is not None and self.intent_regex is not None:
            raise self.validation_error(
                "you cannot specify both 'intent' and 'intent_regex' "
                "properties at the same time"
            )

    def get_intent(self, intents: List[WitIntent]) -> WitIntent:
        for intent in intents:
            if self.is_match(intent.name, intent.confidence):
                return intent

    def is_match(self, intent_name: str, confidence: Real):
        if not self.intent_regex and not self.intent:
            if self.min_confidence <= confidence <= self.max_confidence:
                return True
            return False

        match = False
        if self.intent_regex and RegexTrigger.search_regex(
            self.intent_regex, intent_name, ignorecase=True
        ):
            match = True
        elif isinstance(self.intent, str) and self.intent == intent_name:
            match = True
        elif isinstance(self.intent, list) and intent_name in self.intent:
            match = True

        if match and self.min_confidence <= confidence <= self.max_confidence:
            return True

        return False
