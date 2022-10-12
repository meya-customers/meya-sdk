import re

_to_camel_case_pattern = re.compile(r"_[a-z]")


def _to_camel_case_repl(match: re.Match) -> str:
    return match.group(0)[1].upper()


_from_camel_case_pattern = re.compile(r"[A-Z]")


def _from_camel_case_repl(match: re.Match) -> str:
    return f"_{match.group(0).lower()}"


def to_camel_case(original: str) -> str:
    return re.sub(_to_camel_case_pattern, _to_camel_case_repl, original)


def from_camel_case(camel_case: str) -> str:
    return re.sub(_from_camel_case_pattern, _from_camel_case_repl, camel_case)


def to_camel_case_dict_keys(old_dict: dict) -> dict:
    new_dict = {}
    for key, value in old_dict.items():
        if isinstance(value, dict):
            new_value = to_camel_case_dict_keys(value)
        else:
            new_value = value

        if isinstance(key, str):
            new_dict[to_camel_case(key)] = new_value
        else:
            new_dict[key] = new_value
    return new_dict


def from_camel_case_dict_keys(old_dict: dict) -> dict:
    new_dict = {}
    for key, value in old_dict.items():
        if isinstance(value, dict):
            new_value = from_camel_case_dict_keys(value)
        else:
            new_value = value

        if isinstance(key, str):
            new_dict[from_camel_case(key)] = new_value
        else:
            new_dict[key] = new_value
    return new_dict
