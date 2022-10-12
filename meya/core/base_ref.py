from dataclasses import dataclass


@dataclass
class BaseRef:
    ref: str

    def __post_init__(self):
        self.ref = self.ref.strip()

    def __str__(self):
        return self.ref
