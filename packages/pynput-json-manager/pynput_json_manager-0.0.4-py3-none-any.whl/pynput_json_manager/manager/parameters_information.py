import json
import os
from typing import Any, Dict, Tuple


def convert_type_dict(type_of: Dict[str, str]) -> Dict[str, Any]:
    """
    convert json types to python types:

    Args:
        type_of: dict of json types for each key
    """
    output = {}
    for key, value in type_of.items():
        if value == "int":
            output[key] = int
        elif value == "float":
            output[key] = float
        elif value == "bool":
            output[key] = bool
    return output


def get_inforamtion(path_to_information: str) -> Tuple[Any]:
    with open(os.path.join(path_to_information, "shortcuts.json"), "r") as f:
        shortcuts = json.load(f)
    with open(
        os.path.join(path_to_information, "general_information_keys.json"), "r"
    ) as f:
        general_information_keys = json.load(f)["keys"]
    with open(os.path.join(path_to_information, "type_of.json"), "r") as f:
        type_of = convert_type_dict(json.load(f))
    with open(os.path.join(path_to_information, "default_values.json"), "r") as f:
        default_values = json.load(f)
    return shortcuts, general_information_keys, type_of, default_values
