from pathlib import Path
from typing import Optional
import json
import os


def folder_management(
    exp_folder: str, path_to_information: Optional[str] = None
) -> None:
    """
    check if folders exist and creates them otherwise
    """
    if not os.path.isdir(exp_folder):
        Path(exp_folder).mkdir(parents=True, exist_ok=True)
    if path_to_information is not None:
        if not os.path.isdir(path_to_information):
            Path(path_to_information).mkdir(parents=True, exist_ok=True)
            with open(
                os.path.join(path_to_information, "default_values.json"), "w"
            ) as json_file:
                json.dump(
                    {"experiment is running": False, "experiment is done": False},
                    json_file,
                )
            with open(
                os.path.join(path_to_information, "possible_values.json"), "w"
            ) as json_file:
                json.dump({}, json_file)
            with open(
                os.path.join(path_to_information, "shortcuts.json"), "w"
            ) as json_file:
                json.dump(
                    {"experiment is running": "running", "experiment is done": "done"},
                    json_file,
                )
            with open(
                os.path.join(path_to_information, "general_information_keys.json"), "w"
            ) as json_file:
                json.dump(
                    {"keys": ["experiment is running", "experiment is done"]}, json_file
                )
            with open(
                os.path.join(path_to_information, "precision.json"), "w"
            ) as json_file:
                json.dump({}, json_file)
            with open(
                os.path.join(path_to_information, "type_of.json"), "w"
            ) as json_file:
                json.dump(
                    {"experiment is running": "bool", "experiment is done": "bool"},
                    json_file,
                )
