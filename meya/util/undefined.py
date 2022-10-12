from jinja2 import Undefined
from jinja2 import UndefinedError


class StrictUndefined(Undefined):
    __eq__ = Undefined._fail_with_undefined_error
    __ne__ = Undefined._fail_with_undefined_error
    __hash__ = Undefined._fail_with_undefined_error
    __str__ = Undefined._fail_with_undefined_error
    __len__ = Undefined._fail_with_undefined_error
    __nonzero__ = Undefined._fail_with_undefined_error
    __bool__ = Undefined._fail_with_undefined_error
    __repr__ = Undefined._fail_with_undefined_error


class MissingUndefinedError(UndefinedError):
    pass


MISSING_UNDEFINED = StrictUndefined(exc=MissingUndefinedError)
