from enum import Enum
from enum import EnumMeta


class SimpleEnum(Enum):
    def __repr__(self):
        # Don't show angle brackets or the enum value, because that turns
        # pytest error results into invalid Python
        return self.__str__()


class SimpleEnumMeta(EnumMeta):
    def __contains__(cls, member):
        if not isinstance(member, Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)
