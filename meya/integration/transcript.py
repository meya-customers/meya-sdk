from dataclasses import dataclass
from meya.element.field import meta_field
from meya.integration.element import Integration


@dataclass
class TranscriptMixin(Integration):
    is_abstract: bool = meta_field(value=True)

    def __init__(self, *args, **kwargs):
        import warnings

        warnings.warn(
            "Use `CspIntegration` instead of `TranscriptMixin`",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)
