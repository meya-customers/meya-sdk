from dataclasses import dataclass
from datetime import timedelta
from meya.element.field import element_field
from meya.text.component.ask.ask import AskComponent
from meya.twilio.voice.event.gather import GatherInput
from meya.twilio.voice.event.gather import SpeechModel
from typing import Optional


@dataclass
class TwilioVoiceGatherComponent(AskComponent):
    """
    # Gather
    ## Collect digits or transcribe speech during a call.

    ## Parameters:

    #### input: Specify which inputs Twilio should accept with the input attribute.
    - dtmf
    - speech
    - dtmf speech
    #### timeout: Wait for the caller to press another digit or say another word before it sends data to your action URL.
    #### profanity_filter: Filter profanities out of your speech transcription.
    #### finish_on_key: Set a value that your caller can press to submit their digits.
    #### num_digits: Set the number of digits you expect from your caller.
    #### language: Specifies the language should recognize from your caller.
    #### hints: Improve recognition of the words or phrases you expect from your callers.
    #### speech_timeout: Wait before it stops its speech recognition.
    #### speech_model: Specifies the model that is best suited for your use case to improve the accuracy of speech to text.
    - default
    - numbers_and_commands
    - phone_call
    #### enhanced: Improve the accuracy of transcription results.
    """

    input: GatherInput = element_field()
    timeout: Optional[timedelta] = element_field(
        default=None
    )  # TODO Pick a field name that doesn't conflict with base element timeout
    profanity_filter: Optional[bool] = element_field(default=None)
    finish_on_key: Optional[str] = element_field(default=None)
    num_digits: Optional[int] = element_field(default=None)
    language: Optional[str] = element_field(default=None)
    hints: Optional[str] = element_field(default=None)
    speech_timeout: Optional[timedelta] = element_field(default=None)
    speech_model: Optional[SpeechModel] = element_field(default=None)
    enhanced: Optional[bool] = element_field(default=None)
