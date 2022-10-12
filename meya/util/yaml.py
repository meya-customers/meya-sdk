import ruamel.yaml.comments

from io import StringIO
from ruamel.yaml import YAML

round_trip_yaml = YAML(typ="rt")
round_trip_yaml.indent = 2
round_trip_yaml.sequence_indent = 4
round_trip_yaml.sequence_dash_offset = 2

# Export here to avoid __all__ import warning
CommentedBase = ruamel.yaml.comments.CommentedBase
LineCol = ruamel.yaml.comments.LineCol


def from_yaml(stream):
    return round_trip_yaml.load(stream)


def from_multi_yaml(stream):
    return round_trip_yaml.load_all(stream)


def to_yaml(obj, stream=None):
    if stream is None:
        stream = StringIO()
    round_trip_yaml.dump(obj, stream)
    if isinstance(stream, StringIO):
        return stream.getvalue()


def to_multi_yaml(obj, stream=None):
    if stream is None:
        stream = StringIO()
    round_trip_yaml.dump_all(obj, stream)
    if isinstance(stream, StringIO):
        return stream.getvalue()
