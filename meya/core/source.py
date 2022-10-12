from dataclasses import dataclass


@dataclass
class Source:
    file_path: str
    text: str
