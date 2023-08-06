from typing import List, Dict
from .parameters_information import get_inforamtion, convert_type_dict
from .update_parameters import save_types
import os
import json


def print_keys(general_information_keys: List[str], shortcuts: Dict[str, str]) -> None:
    """
    fancy print of the main keys and their corresponding shortcuts

    Args:
        general_information_keys: list of the keys as strings
        shortcuts: dict that maps a key to its shortcut
    """
    for key, (_, values) in zip(general_information_keys, shortcuts.items()):
        print(
            f"\033[95m{key}\033[00m"
            + " " * (35 - len(key))
            + f"\033[92m{values}\033[00m"
        )


def update_all_exp_jsons(exp_folder: str, key: str) -> None:
    """
    updates the remaining json files after deletion

    args:
        key: key of the json file to delete
        exp_folder: path to the json files to edit
    """
    for file in os.listdir(exp_folder):
        if ".json" in file:
            with open(os.path.join(exp_folder, file), "r") as f:
                data = json.load(f)
            if key in data:
                data.pop(key, None)
            with open(os.path.join(exp_folder, file), "w") as json_file:
                json.dump(data, json_file)


def delete_a_key(
    exp_folder: str, path_to_information: str = os.path.abspath(__file__)
) -> None:
    """
    delete a key in all json files.
    The key to delete is requested by this function during execution.

    args:
        path_to_information: path to the files that define the keys of our experiments
        exp_folder: path to the json files to edit
    """
    with open(os.path.join(path_to_information, "shortcuts.json"), "r") as f:
        shortcuts = json.load(f)
    with open(
        os.path.join(path_to_information, "general_information_keys.json"), "r"
    ) as f:
        general_information_keys = json.load(f)
    with open(os.path.join(path_to_information, "type_of.json"), "r") as f:
        type_of = convert_type_dict(json.load(f))
    with open(os.path.join(path_to_information, "default_values.json"), "r") as f:
        default_values = json.load(f)
    with open(os.path.join(path_to_information, "possible_values.json"), "r") as f:
        possible_values = json.load(f)
    print_keys(general_information_keys["keys"], shortcuts)

    reverted_shortcuts = dict((v, k) for k, v in shortcuts.items())

    key_to_delete = input("which key do you want to delete (enter shortcut)? ")
    while key_to_delete in reverted_shortcuts:
        key_to_delete = reverted_shortcuts[key_to_delete]
        if key_to_delete in shortcuts:
            shortcuts.pop(key_to_delete, None)
        if key_to_delete in general_information_keys["keys"]:
            general_information_keys["keys"].remove(key_to_delete)
        if key_to_delete in type_of:
            type_of.pop(key_to_delete, None)
        if key_to_delete in default_values:
            default_values.pop(key_to_delete, None)
        if key_to_delete in possible_values:
            possible_values.pop(key_to_delete, None)
        with open(
            os.path.join(path_to_information, "shortcuts.json"), "w"
        ) as json_file:
            json.dump(shortcuts, json_file)
        with open(
            os.path.join(path_to_information, "general_information_keys.json"), "w"
        ) as json_file:
            json.dump(general_information_keys, json_file)
        save_types(d=type_of, path_to_information=path_to_information)
        with open(
            os.path.join(path_to_information, "default_values.json"), "w"
        ) as json_file:
            json.dump(default_values, json_file)
        with open(
            os.path.join(path_to_information, "possible_values.json"), "w"
        ) as json_file:
            json.dump(possible_values, json_file)
        update_all_exp_jsons(exp_folder=exp_folder, key=key_to_delete)
        key_to_delete = input("which key do you want to delete (enter shortcut)? ")
