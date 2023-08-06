from .parameters_information import get_inforamtion, convert_type_dict
import os
import json
from typing import Dict, Any


def add_new_key(path_to_information: str) -> str:
    _, general_information_keys, _, _ = get_inforamtion(
        path_to_information=path_to_information
    )
    new_key = input("please enter the new key                               :")
    while new_key in general_information_keys:
        new_key = input("please enter the new key (previous key already exists) :")
    return new_key


def get_type() -> str:
    new_type = input("please provide the type (int, bool, float or str)      :")
    return new_type


def get_precision(path_to_information: str, new_key: str) -> None:
    precision = input("please provide the precision (0.1)      :")
    with open(os.path.join(path_to_information, "precision.json"), "r") as f:
        precisions = json.load(f)
    precisions[new_key] = precision
    with open(os.path.join(path_to_information, "precision.json"), "w") as json_file:
        json.dump(precisions, json_file)


def get_default(new_type) -> str:
    new_value = input("please provide the default value                       :")
    return new_value


def get_shortcut() -> str:
    new_shortcut = input("please provide the shortcut (else press enter)         :")
    return new_shortcut


def save_key_dict(exp_folder: str, d: Dict[str, Any], name: str) -> None:
    with open(os.path.join(exp_folder, name), "w") as json_file:
        json.dump(d, json_file)


def save_types(path_to_information: str, d: Dict[str, Any]) -> None:
    data = {}
    for key, values in d.items():
        if values == bool:
            data[key] = "bool"
        elif values == float:
            data[key] = "float"
        elif values == int:
            data[key] = "int"
        else:
            data[key] = values
    save_key_dict(exp_folder=path_to_information, d=data, name="type_of.json")


def insert_key_value(
    d: Dict[Any, Any], key: Any, value: Any, k: int = 2
) -> Dict[Any, Any]:
    """
    generic way of inserting at specific place in ordered dict
    """
    list_keys = list(d.keys())
    list_keys.insert(k, key)
    output = {}
    for key in list_keys:
        if key in d:
            output[key] = d[key]
        else:
            output[key] = value
    return output


def add_new_parameter(exp_folder: str, path_to_information: str) -> None:
    """
    adds a new parameter to the exp options

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
    """
    print("\n+------------------------------------------------------+")
    print("| Instructions for new parameter in experiments:       |")
    print("| You will be asked to give the parameter key, type    |")
    print("| and default value. Consequently, the .json files     |")
    print("| will be updated adequately.                          |")
    print("+------------------------------------------------------+\n")
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

    new_key = add_new_key(path_to_information=path_to_information)
    new_type = get_type()
    if new_type == "float":
        get_precision(path_to_information=path_to_information, new_key=new_key)
    new_value = get_default(new_type)
    new_shortcut = get_shortcut()
    if new_shortcut == "":
        new_shortcut = new_key

    general_information_keys.insert(2, new_key)
    save_key_dict(
        exp_folder=path_to_information,
        d={"keys": general_information_keys},
        name="general_information_keys.json",
    )
    default_values = insert_key_value(d=default_values, key=new_key, value=new_value)
    save_key_dict(
        exp_folder=path_to_information, d=default_values, name="default_values.json"
    )
    shortcuts = insert_key_value(d=shortcuts, key=new_key, value=new_shortcut)
    save_key_dict(exp_folder=path_to_information, d=shortcuts, name="shortcuts.json")
    if new_type != "str":
        type_of = insert_key_value(d=type_of, key=new_key, value=new_type)
        save_types(path_to_information=path_to_information, d=type_of)
    data_value = "-"
    if new_value == "false":
        data_value = False
    for json_file in os.listdir(exp_folder):
        if ".json" in json_file:
            with open(os.path.join(exp_folder, json_file), "r") as f:
                data = json.load(f)
            data = insert_key_value(d=data, key=new_key, value=data_value)
            with open(os.path.join(exp_folder, json_file), "w") as json_file:
                json.dump(data, json_file)
