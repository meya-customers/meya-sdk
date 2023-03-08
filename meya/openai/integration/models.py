from meya.util.enum import SimpleEnum
from meya.util.enum import SimpleEnumMeta
from typing import List
from typing import Union


class ModelEnumMixin:
    @classmethod
    def choices(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def from_str(
        cls, model: str
    ) -> Union["OpenaiTextModel", "OpenaiEmbeddingModel"]:
        try:
            return cls(model)
        except ValueError:
            pass

        try:
            return cls.__members__[model]
        except KeyError:
            raise ValueError(f"Invalid model: {model}")


class OpenaiTextModel(ModelEnumMixin, SimpleEnum, metaclass=SimpleEnumMeta):
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    TEXT_DAVINCI_003 = "text-davinci-003"
    TEXT_DAVINCI_002 = "text-davinci-002"
    TEXT_CURIE_001 = "text-curie-001"
    TEXT_BABBAGE_001 = "text-babbage-001"
    TEXT_ADA_001 = "text-ada-001"

    @classmethod
    def max_tokens(cls, model: "OpenaiTextModel") -> int:
        max_prompts = {
            # OpenAI model limits: https://platform.openai.com/docs/models/gpt-3-5
            OpenaiTextModel.GPT_3_5_TURBO_0301: 4096,
            OpenaiTextModel.GPT_3_5_TURBO: 4096,
            OpenaiTextModel.TEXT_DAVINCI_003: 4000,
            OpenaiTextModel.TEXT_DAVINCI_002: 4000,
            OpenaiTextModel.TEXT_CURIE_001: 2048,
            OpenaiTextModel.TEXT_BABBAGE_001: 2048,
            OpenaiTextModel.TEXT_ADA_001: 2048,
        }
        return max_prompts.get(model, 2048)

    @classmethod
    def completion_models(cls) -> List["OpenaiTextModel"]:
        return [
            cls.TEXT_DAVINCI_003,
            cls.TEXT_DAVINCI_002,
            cls.TEXT_CURIE_001,
            cls.TEXT_BABBAGE_001,
            cls.TEXT_ADA_001,
        ]

    @classmethod
    def chat_models(cls) -> List["OpenaiTextModel"]:
        return [cls.GPT_3_5_TURBO_0301, cls.GPT_3_5_TURBO]


class OpenaiEmbeddingModel(
    ModelEnumMixin, SimpleEnum, metaclass=SimpleEnumMeta
):
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

    @classmethod
    def dimensions(cls, model: "OpenaiEmbeddingModel") -> int:
        dimensions = {
            OpenaiEmbeddingModel.TEXT_EMBEDDING_ADA_002: 1536,
        }
        return dimensions.get(model, 1536)
