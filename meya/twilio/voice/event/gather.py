from dataclasses import dataclass
from datetime import timedelta
from meya.entry.field import entry_field
from meya.text.event.ask import AskEvent
from meya.util.enum import SimpleEnum
from typing import Optional


class GatherInput(SimpleEnum):
    DTMF = "dtmf"
    SPEECH = "speech"
    DTMF_SPEECH = "dtmf speech"


class SpeechModel(SimpleEnum):
    DEFAULT = "default"
    NUMBERS_AND_COMMANDS = "numbers_and_commands"
    PHONE_CALL = "phone_call"


@dataclass
class TwilioVoiceGatherEvent(AskEvent):
    input: GatherInput = entry_field()
    timeout: Optional[timedelta] = entry_field(default=None)
    profanity_filter: Optional[bool] = entry_field(default=None)
    finish_on_key: Optional[str] = entry_field(default=None)
    num_digits: Optional[int] = entry_field(default=None)
    language: Optional[str] = entry_field(default=None)
    hints: Optional[str] = entry_field(default=None)
    speech_timeout: Optional[timedelta] = entry_field(default=None)
    speech_model: Optional[SpeechModel] = entry_field(default=None)
    enhanced: Optional[bool] = entry_field(default=None)
