from dataclasses import dataclass
from meya.core.source_location import SourceLocation
from ruamel.yaml.comments import CommentedMap


@dataclass
class Template:
    content: CommentedMap
    single_document: bool
    source_location: SourceLocation
