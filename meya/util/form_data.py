from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Union

if TYPE_CHECKING:
    from aiohttp import FormData


"""
------------------------------------------------------------------------------
    This class is used for converting python dicts to FormData
    FormData is used when you need to send binary data together with json
    
    This class is really important when you need to convert nested dicts to 
    FormData, for example:
    {
        key: {
            nested_key: value
        }
    }
    This dict needs to be translated to:
    key[nested_key] = value
    
    This is what this class does
    
    BinaryFile is helper class for generating binary data with correct filename
    and content_type, directly from dict
------------------------------------------------------------------------------
"""


@dataclass
class BinaryFile:
    filename: str
    content_type: str
    data: bytes


def parse_dict_as_form_data(payload: Union[Dict[str, Any]]) -> "FormData":
    from aiohttp import FormData

    def parse_obj(
        obj: Union[Dict[str, Any], List[Any], int, float, str], parent_key=None
    ):
        result = {}
        if isinstance(obj, Dict):
            for k, v in obj.items():
                key = k
                if parent_key:
                    key = f"{parent_key}[{k}]"
                result.update(parse_obj(v, key))

        if isinstance(obj, List):
            for k, v in enumerate(obj):
                parsed_list_object = parse_obj(v)
                if isinstance(parsed_list_object, dict):
                    for child_k, child_v in parsed_list_object.items():
                        result.update(
                            {
                                f"{parent_key}[{k}][{child_k}]": parse_obj(
                                    child_v
                                )
                            }
                        )
                else:
                    result.update({f"{parent_key}[{k}]": parse_obj(v)})

        if (
            isinstance(obj, str)
            or (isinstance(obj, int) and not isinstance(obj, bool))
            or isinstance(obj, float)
            or isinstance(obj, BinaryFile)
        ):
            if parent_key:
                return {f"{parent_key}": obj}
            return obj

        if isinstance(obj, bool):
            parsed_bool = "true" if obj else "false"
            if parent_key:
                return {f"{parent_key}": parsed_bool}
            return parsed_bool

        return result

    form_data = FormData(quote_fields=False)
    parsed_payload = parse_obj(payload)
    for key, value in parsed_payload.items():
        if isinstance(value, BinaryFile):
            form_data.add_field(
                name=key,
                value=value.data,
                filename=value.filename,
                content_type=value.content_type,
            )
            continue
        form_data.add_field(name=key, value=value)

    return form_data
